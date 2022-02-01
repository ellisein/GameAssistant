import os
import asyncio
import aiohttp
from urllib import parse
from functools import wraps

from .utils import Singleton


def make_query(params):
	queryset = []
	for k, v in params.items():
		queryset.append(f'{k}={v}')
	return '?' + '&'.join(queryset)

def encode(base, url):
    parsed = parse.urlparse(make_query(url))
    parsed = parse.parse_qs(parsed.query)
    encoded = "{}?{}".format(base, parse.urlencode(parsed, doseq=True))
    return encoded


class API_base(metaclass=Singleton):
	@staticmethod
	async def _get(url):
		async with aiohttp.ClientSession() as session:
			async with session.get(url) as response:
				if response.status == 200:
					return await response.json()
				else:
					return None


class API_blizzard(API_base):
	BASE_URL = 'https://kr.api.blizzard.com'
	OAUTH_URL = 'https://kr.battle.net/oauth'
	THUMBNAIL_URL = 'https://render-kr.worldofwarcraft.com/character'
	_token = None

	@classmethod
	def init_access_token(cls):
		return asyncio.run(cls.renew_access_token())

	@classmethod
	async def renew_access_token(cls):
		url = encode(f'{cls.OAUTH_URL}/token', {
			'grant_type': 'client_credentials',
			'client_id': os.getenv('BLIZZARD_API_CLIENT_ID'),
			'client_secret': os.getenv('BLIZZARD_API_CLIENT_SECRET')
		})

		async with aiohttp.ClientSession() as session:
			async with session.post(url) as response:
				if response.status == 200:
					token = await response.json()
					if cls._token != token['access_token']:
						cls._token = token['access_token']
						return True
		return False

	@classmethod
	async def check_access_token(cls):
		if cls._token is None:
			ret = await cls.renew_access_token()
			return ret

		url = encode(f'{cls.OAUTH_URL}/check_token', {
			'token': cls._token
		})

		async with aiohttp.ClientSession() as session:
			async with session.get(url) as response:
				if response.status == 200:
					return True
				else:
					ret = await cls.renew_access_token()
					return ret
		return False

	@classmethod
	async def get(cls, url, repeat=True):
		if cls._token is None:
			await cls.renew_access_token()

		ret = await cls._get(url)
		if ret:
			return ret
		else:
			if not repeat and await cls.check_access_token():
				return await cls.get(url, repeat=False)
			return None

	@classmethod
	async def get_profile(cls, realm_name, character_name):
		url = encode(f'{cls.BASE_URL}/profile/wow/character/{realm_name}/{character_name}', {
			'access_token': cls._token,
			'namespace': 'profile-kr',
			'locale': 'ko_KR'
		})

		return await cls.get(url)

	@classmethod
	async def get_media(cls, realm_name, character_name):
		url = encode(f'{cls.BASE_URL}/profile/wow/character/{realm_name}/{character_name}/character-media', {
			'access_token': cls._token,
			'namespace': 'profile-kr',
			'locale': 'ko_KR'
		})

		return await cls.get(url)

	@classmethod
	async def get_equipment(cls, realm_name, character_name):
		url = encode(f'{cls.BASE_URL}/profile/wow/character/{realm_name}/{character_name}/equipment', {
			'access_token': cls._token,
			'namespace': 'profile-kr',
			'locale': 'ko_KR'
		})

		return await cls.get(url)

	@classmethod
	async def get_item_media(cls, item_id):
		url = encode(f'{cls.BASE_URL}/data/wow/media/item/{item_id}', {
			'access_token': cls._token,
			'namespace': 'static-kr',
			'locale': 'ko_KR'
		})

		return await cls.get(url)

	@classmethod
	async def get_mythic_keystone_profile(cls, realm_name, character_name):
		url = encode(f'{cls.BASE_URL}/profile/wow/character/{realm_name}/{character_name}/mythic-keystone-profile', {
			'access_token': cls._token,
			'namespace': 'profile-kr',
			'locale': 'ko_KR'
		})

		return await cls.get(url)

	@classmethod
	async def get_realm(cls):
		url = encode(f'{cls.BASE_URL}/data/wow/realm/index', {
			'access_token': cls._token,
			'namespace': 'dynamic-kr',
			'locale': 'ko_KR'
		})

		return await cls.get(url)

	@classmethod
	async def get_specializations(cls, realm_name, character_name):
		url = encode(f'{cls.BASE_URL}/profile/wow/character/{realm_name}/{character_name}/specializations', {
			'access_token': cls._token,
			'namespace': 'profile-kr',
			'locale': 'ko_KR'
		})

		return await cls.get(url)

	@classmethod
	async def get_spell_media(cls, spell_id):
		url = encode(f'{cls.BASE_URL}/data/wow/media/spell/{spell_id}', {
			'access_token': cls._token,
			'namespace': 'static-kr',
			'locale': 'ko_KR'
		})

		return await cls.get(url)

	@classmethod
	async def get_mythic_keystone_periods(cls):
		url = encode(f'{cls.BASE_URL}/data/wow/mythic-keystone/period/index', {
			'access_token': cls._token,
			'namespace': 'dynamic-kr',
			'locale': 'ko_KR'
		})

		return await cls.get(url)

	@classmethod
	async def get_mythic_keystone_period(cls, period_id):
		url = encode(f'{cls.BASE_URL}/data/wow/mythic-keystone/period/{period_id}', {
			'access_token': cls._token,
			'namespace': 'dynamic-kr',
			'locale': 'ko_KR'
		})

		return await cls.get(url)

	@classmethod
	async def get_affix_media(cls, affix_id):
		url = encode(f'{cls.BASE_URL}/data/wow/media/keystone-affix/{affix_id}', {
			'access_token': cls._token,
			'namespace': 'static-kr',
			'locale': 'ko_KR'
		})

		return await cls.get(url)


class API_raiderio(API_base):
	BASE_URL = 'https://raider.io/api/v1'

	@classmethod
	async def get_character(cls, realm_name, character_name):
		url = encode(f'{cls.BASE_URL}/characters/profile', {
			'region': 'kr',
			'realm': realm_name,
			'name': character_name,
			'fields': 'mythic_plus_ranks',
		})

		return await cls._get(url)

	@classmethod
	async def get_mythic_keystone_affixes(cls):
		url = encode(f'{cls.BASE_URL}/mythic-plus/affixes', {
			'region': 'kr',
			'locale': 'ko',
		})

		return await cls._get(url)


class API_minecraft(API_base):
	@classmethod
	async def get_uuid(cls, username):
		url = f'https://api.mojang.com/users/profiles/minecraft/{username}'
		return await cls._get(url)

	@classmethod
	async def get_name_history(cls, uuid):
		url = f'https://api.mojang.com/user/profiles/{uuid}/names'
		return await cls._get(url)

	@classmethod
	async def get_profile(cls, uuid):
		url = f'https://sessionserver.mojang.com/session/minecraft/profile/{uuid}'
		return await cls._get(url)
