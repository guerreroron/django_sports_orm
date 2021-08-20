from django.shortcuts import render, redirect
from .models import League, Team, Player
from django.db.models import Count

from . import team_maker

def index(request):
	context = {
		"leagues" : League.objects.all(),
		"teams" : Team.objects.all(),
		"players" : Player.objects.all()
	}
	return render(request, "leagues/index.html", context)

def lvl1(request):
	names_for_16 = [
		"Alexander",
		"Wyatt"
	]
	
	context = {
		"baseball_leagues" : League.objects.filter(sport__contains="baseball"),
		"women_leagues" : League.objects.filter(name__contains="women"),
		"hockey_leagues" : League.objects.filter(sport__contains="hockey"),
		"not_football_leagues" : League.objects.exclude(sport__contains="football"),
		"conferences_leagues" : League.objects.filter(name__contains="conference"),
		"atlantic_leagues" : League.objects.filter(name__contains="atlantic"),
		"dallas_teams" : Team.objects.filter(location__contains="dallas"),
		"raptors_teams" : Team.objects.filter(team_name__contains="raptors"),
		"location_city_teams" : Team.objects.filter(location__contains="city"),
		"begin_t_teams" : Team.objects.filter(team_name__startswith="t"),
		"ordered_location_teams" : Team.objects.all().order_by("location"),
		"ordered_name_reverse_teams" : Team.objects.all().order_by("-team_name"),
		"lastname_cooper_player" : Player.objects.filter(last_name__contains="cooper"),
		"firstname_joshua_player" : Player.objects.filter(first_name__contains="joshua"),
		"lastname_cooper_not_joshua_player" : Player.objects.filter(last_name__contains="cooper").exclude(first_name__contains="joshua"),	
		"firstname_alexander_wyatt_player" : Player.objects.all().filter(first_name__in=names_for_16)
	}
	return render(request, "leagues/lvl1.html", context)

def lvl2(request):
	context = {
		"atlantic_soccer_league_teams" : Team.objects.filter(league__name='Atlantic Soccer Conference'),
		'boston_penguins_players': Player.objects.filter(curr_team=Team.objects.get(location='Boston', team_name='Penguins')),
		'players_in_international_collegiate_baseball_conference': Player.objects.filter(curr_team__in=Team.objects.filter(league__name='International Collegiate Baseball Conference')).order_by('curr_team__location', 'first_name'),
		'players_in_american_conference_amateur_football_with_lastname_lopez': Player.objects.filter(curr_team__in=Team.objects.filter(league=League.objects.get(name='American Conference of Amateur Football'))).filter(last_name='Lopez').order_by('first_name'),
		'all_football_players': Player.objects.filter(curr_team__in=Team.objects.filter(league__in=League.objects.filter(sport='Football'))).order_by('curr_team__team_name','last_name'),
		'teams_who_player_is_sophia': Team.objects.filter(curr_players__in=Player.objects.filter(first_name='Sophia')).order_by('team_name'),
		'leagues_who_player_is_sophia': League.objects.filter(teams__in=Team.objects.filter(curr_players__in=Player.objects.filter(first_name='Sophia'))).order_by('name'),
		'players_last_name_flores_except_washington_roughriders': Player.objects.filter(last_name='Flores').exclude(curr_team=Team.objects.get(team_name='Roughriders', location='Washington')).order_by('curr_team__team_name','curr_team__location', 'first_name'),
		'all_teams_where_samuel_evans_has_played': Player.objects.get(first_name='Samuel', last_name='Evans').all_teams.all().order_by('team_name'),
		'all_players_has_played_in_manitoba': Player.objects.filter(all_teams__team_name='Tiger-Cats', all_teams__location='Manitoba').order_by('last_name'),
		'all_pased_players_in_wichita_vikins': Player.objects.filter(all_teams__team_name='Vikings', all_teams__location='Wichita').exclude(curr_team__team_name='Vikings').order_by('last_name'),
		'all_teams_where_jacob_gray_played_before_join_oregon_colts': Player.objects.get(first_name='Jacob', last_name='Gray').all_teams.all().exclude(team_name='Colts', location='Oregon'),
		'all_players_named_joshua_played_in_atlan_feder_amateur_baseball': Player.objects.filter(first_name='Joshua', all_teams__league__name='Atlantic Federation of Amateur Baseball Players'),
		'all_teams_have_had_12_or_more_players_past_present': Team.objects.annotate(ply=Count("all_players")).filter(ply__gt=11).order_by('team_name'),
		'all_players_sorted_by_the_number_of_teams_have_played': Player.objects.annotate(played=Count("all_teams")).order_by("played")

	}
	return render(request, "leagues/lvl2.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")