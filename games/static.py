from django.conf import settings
from django.core.files.base import ContentFile

import os
import asyncio
import MinePI
from io import BytesIO
from PIL import Image
from datetime import datetime

from .api import API_blizzard
from .utils import Singleton
from .models import WowItemMedia, WowSpellMedia, WowAffixMedia
from .models import Minecraft3dTexture


class static_wow(metaclass=Singleton):
	_REALMS = list()
	_MK_CUR_ENDTIME = None
	_MK_CUR_CONTEXT = None

	@classmethod
	def load_realm(cls):
		cls._REALMS.clear()
		realm = asyncio.run(API_blizzard.get_realm())
		if realm:
			for r in realm['realms']:
				cls._REALMS.append({'KR': r['name'], 'EN': r['slug']})

	@classmethod
	def get_realms(cls):
		return cls._REALMS

	@classmethod
	def get_mythic_keystone_affixes(cls):
		if cls._MK_CUR_ENDTIME and datetime.now().timestamp() < cls._MK_CUR_ENDTIME:
			return cls._MK_CUR_CONTEXT
		return None

	@classmethod
	def set_mythic_keystone_affixes(cls, endtime, context):
		cls._MK_CUR_ENDTIME = endtime
		cls._MK_CUR_CONTEXT = context

	@staticmethod
	def get_item_media(items):
		item_media = dict()
		for item in items:
			item_id = item['item']['id']
			media = WowItemMedia()
			try:
				media = WowItemMedia.objects.get(pk=item_id)
			except WowItemMedia.DoesNotExist:
				c_media = asyncio.run(API_blizzard.get_item_media(item_id))
				media.item_id = item_id
				media.media_url = c_media['assets'][0]['value']
				media.save()
			item_media[item_id] = media.media_url
		return item_media

	@staticmethod
	def get_item_detail(items, item_media):
		item_detail = dict()
		item_detail_list = list()
		for i in items:
			item_detail[i['slot']['type']] = {
				'id': i['item']['id'],
				'slot': i['slot']['type'],
				'name': i['name'],
				'media': item_media[i['item']['id']],
			}
		for slot in static_wow.ITEM_SLOT_TYPES:
			if slot in item_detail:
				item_detail_list.append(item_detail[slot])
			else:
				item_detail_list.append(None)
		return item_detail_list

	@staticmethod
	def get_spell_media(spell_id):
		media = WowSpellMedia()
		try:
			media = WowSpellMedia.objects.get(pk=spell_id)
		except WowSpellMedia.DoesNotExist:
			c_media = asyncio.run(API_blizzard.get_spell_media(spell_id))
			media.spell_id = spell_id
			media.media_url = c_media['assets'][0]['value']
			media.save()
		return media.media_url

	@staticmethod
	def get_affix_media(affix_id):
		media = WowAffixMedia()
		try:
			media = WowAffixMedia.objects.get(pk=affix_id)
		except WowAffixMedia.DoesNotExist:
			c_media = asyncio.run(API_blizzard.get_affix_media(affix_id))
			media.affix_id = affix_id
			media.media_url = c_media['assets'][0]['value']
			media.save()
		return media.media_url

	@classmethod
	def get_talent_summary(cls, specializations, spec_id):
		talents = list()
		for spec in specializations:
			if spec['specialization']['id'] == spec_id:
				for talent in spec['talents']:
					talents.append({
						'id': talent['spell_tooltip']['spell']['id'],
						'name': talent['spell_tooltip']['spell']['name'],
						'media': cls.get_spell_media(talent['spell_tooltip']['spell']['id']),
					})
		return talents

	@classmethod
	def get_affix_detail(cls, affixes):
		ret = list()
		for affix in affixes:
			ret.append({
				'name': affix['name'],
				'description': affix['description'],
				'media': cls.get_affix_media(affix['id']),
			})
		return ret

	CLASS_COLOR = {
		1: '#C69B6D', # Warrior
		2: '#F48CBA', # Paladin
		3: '#AAD372', # Hunter
		4: '#FFF468', # Rogue
		5: '#FFFFFF', # Priest
		6: '#C41E3A', # Death Knight
		7: '#0070DD', # Shaman
		8: '#3FC7EB', # Mage
		9: '#8788EE', # Warlock
		10: '#00FF98', # Monk
		11: '#FF7C0A', # Druid
		12: '#A330C9', # Demon Hunter
	}

	ITEM_SLOT_TYPES = [
		'HEAD',
		'NECK',
		'SHOULDER',
		'CHEST',
		'WAIST',
		'LEGS',
		'FEET',
		'WRIST',
		'HANDS',
		'FINGER_1',
		'FINGER_2',
		'TRINKET_1',
		'TRINKET_2',
		'BACK',
		'MAIN_HAND',
		'OFF_HAND'
	]

static_wow.load_realm()


class static_minecraft:
	@staticmethod
	async def get_3d_skin(username):
		im = await MinePI.render_3d_skin(username)
		io = BytesIO()
		im.save(io, format='png')
		return ContentFile(io.getvalue(), f'{username}.png')

	@classmethod
	def save_3d_skin(cls, username, url):
		texture = Minecraft3dTexture()
		texture.name = username
		texture.skin = asyncio.run(cls.get_3d_skin(username))
		texture.url = url
		texture.save()
		return texture.skin.url

	@classmethod
	def get_3d_skin_url(cls, username, url):
		try:
			texture = Minecraft3dTexture.objects.get(pk=username)
			if texture.url == url:
				return texture.skin.url
		except Minecraft3dTexture.DoesNotExist:
			return None
		return None
