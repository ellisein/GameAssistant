from django.shortcuts import render, redirect
from django.http import HttpResponse

import ast, base64
import asyncio
from datetime import datetime

from . import utils
from .api import API_blizzard, API_raiderio, API_minecraft
from .static import static_wow, static_minecraft


def get_color(color):
	return f"rgba({color['r']},{color['g']},{color['b']})"

def default(request):
	return redirect('wow/character')

def wow_character(request):
	if request.method == 'GET':
		if 'name' in request.GET and 'realm' in request.GET:
			character_name = request.GET['name']
			character_realm = request.GET['realm']
			c_profile = asyncio.run(API_blizzard.get_profile(character_realm, character_name))
			c_media = asyncio.run(API_blizzard.get_media(character_realm, character_name))
			c_equipment = asyncio.run(API_blizzard.get_equipment(character_realm, character_name))
			c_specializations = asyncio.run(API_blizzard.get_specializations(character_realm, character_name))
			c_mythic = asyncio.run(API_blizzard.get_mythic_keystone_profile(character_realm, character_name))
			c_raider_profile = asyncio.run(API_raiderio.get_character(character_realm, character_name))

			if None not in (c_profile, c_media, c_equipment, c_specializations, c_mythic):
				item_media = static_wow.get_item_media(c_equipment['equipped_items'])
				item_detail = static_wow.get_item_detail(c_equipment['equipped_items'], item_media)
				talent_summary = static_wow.get_talent_summary(c_specializations['specializations'], c_profile['active_spec']['id'])

				context = {
					'load': 'SUCCESS',
					'realms': static_wow.get_realms(character_realm),
					'thumbnail': utils.get_value(c_media['assets'], 'key', 'avatar', 'value'),
					'name': c_profile['name'],
					'realm': c_profile['realm']['name'],
					'guild': c_profile['guild']['name'],
					'race': c_profile['race']['name'],
					'active_spec': c_profile['active_spec']['name'],
					'class': c_profile['character_class']['name'],
					'class_color': static_wow.CLASS_COLOR[c_profile['character_class']['id']],
					'level': c_profile['level'],
					'achievement_points': c_profile['achievement_points'],
					'last_login_date': datetime.fromtimestamp(c_profile['last_login_timestamp']/1000).strftime('%Y.%m.%d'),
					'equipped_item_level': c_profile['equipped_item_level'],
					'average_item_level': c_profile['average_item_level'],
					'equipments': item_detail,
					'talents': talent_summary,
					'mythic_score': round(c_mythic['current_mythic_rating']['rating'], 1)
						if 'current_mythic_rating' in c_mythic else None,
					'mythic_color': get_color(c_mythic['current_mythic_rating']['color'])
						if 'current_mythic_rating' in c_mythic else None,
					'mythic_ranks': c_raider_profile['mythic_plus_ranks']
						if c_raider_profile else None,
				}
			else:
				context = {
					'load': 'FAIL',
					'realms': static_wow.get_realms(character_realm),
				}
		else:
			context = {
				'realms': static_wow.get_realms(),
			}

		context['page_name'] = '월드 오브 워크래프트 > 캐릭터 검색'
		return render(request, 'wow_character.html', context)

	else:
		return HttpResponse(status=405)

def wow_mythic_keystone(request):
	context = static_wow.get_mythic_keystone_affixes()
	if context:
		return render(request, 'wow_mythic_keystone.html', context)

	mk_periods = asyncio.run(API_blizzard.get_mythic_keystone_periods())
	mk_period = asyncio.run(API_blizzard.get_mythic_keystone_period(mk_periods['periods'][-1]['id']))
	mk_current_affix = asyncio.run(API_raiderio.get_mythic_keystone_affixes())

	context = {
		'period_start': datetime.fromtimestamp(mk_period['start_timestamp']/1000).strftime('%Y.%m.%d %H:%M:%S'),
		'period_end': datetime.fromtimestamp(mk_period['end_timestamp']/1000).strftime('%Y.%m.%d %H:%M:%S'),
		'affixes': static_wow.get_affix_detail(mk_current_affix['affix_details']),
	}
	static_wow.set_mythic_keystone_affixes(mk_period['end_timestamp']/1000, context)

	context['page_name'] = '월드 오브 워크래프트 > 신화 쐐기돌'
	return render(request, 'wow_mythic_keystone.html', context)

def anno_calculator(request):
	context = {}
	context['page_name'] = 'ANNO 1800 > 생산시설 계산기'
	return render(request, 'anno_calculator.html', context)

def minecraft_user(request):
	if request.method == 'GET':
		context = {}

		if 'name' in request.GET:
			u_uuid = asyncio.run(API_minecraft.get_uuid(request.GET['name']))

			if u_uuid:
				username = u_uuid['name']
				uuid = u_uuid['id']

				u_history = asyncio.run(API_minecraft.get_name_history(uuid))
				u_profile = asyncio.run(API_minecraft.get_profile(uuid))
				u_profile_encoded = utils.get_value(u_profile['properties'], 'name', 'textures', 'value')
				u_profile_decoded = base64.b64decode(u_profile_encoded).decode('utf-8')
				texture = ast.literal_eval(u_profile_decoded)['textures']['SKIN']['url']

				skin_url = static_minecraft.get_3d_skin_url(username, texture)
				if skin_url is None:
					skin_url = static_minecraft.save_3d_skin(username, texture)

				context = {
					'load': 'SUCCESS',
					'name': username,
					'uuid': uuid,
					'name_history': [history['name'] for history in u_history[:-1]],
					'texture': texture,
					'skin': skin_url,
				}

			else:
				context = {
					'load': 'FAIL',
				}

		context['page_name'] = '마인크래프트 > 유저 스킨 검색'
		return render(request, 'minecraft_user.html', context)

	else:
		return HttpResponse(status=405)
