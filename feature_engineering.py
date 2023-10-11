"""This file generates features from Abstract Meaning Representations and creates a dataset that can be used for multiclass-classification.
"""

import pandas as pd
from collections import Counter
import features

df = pd.read_csv('dataset_with_amrs.txt', sep="\t", header=0)

df = df[["AMR", "Relation"]]

# Deletes all rows with LEX compounds
df = df.loc[df["Relation"] != "LEX"]

numbers_f1 = features.focus_numbers(df)
df['sense_with_numbers'] = numbers_f1 
and_f2 = features.focus_and_or("and", df)
df['and'] = and_f2
or_f3 = features.focus_and_or("or", df)
df['or'] = or_f3
no_numbers_and_or_f4 = features.focus_entity(df)
df['no_numbers_and_or'] = no_numbers_and_or_f4

    
person_f5 = features.focus_word("person", df)
df['person'] = person_f5
capable01_f6 = features.focus_word("capable-01", df)
df['capable-01'] = capable01_f6
relation03_f7 = features.focus_word("relation-03", df)
df['relation-03'] = relation03_f7
game_f8 = features.focus_word("game", df)
df['game'] = game_f8
edge_f9 = features.focus_word("edge", df)
df['edge'] = edge_f9
phase_f10 = features.focus_word("phase", df)
df['phase'] = phase_f10
something_f11 = features.focus_word("something", df)
df['something'] = something_f11
process02_f12 = features.focus_word("process-02", df)
df['process-02'] = process02_f12
plant_f13 = features.focus_word("plant", df)
df['plant'] = plant_f13
possible01_f14 = features.focus_word("possible-01", df)
df['possible-01'] = possible01_f14
lack01_f15 = features.focus_word("lack-01", df)
df['lack-01'] = lack01_f15
water_f16 = features.focus_word("water", df)
df['water'] = water_f16
juice_f17 = features.focus_word("juice", df)
df['juice'] = juice_f17
sequence01_f18 = features.focus_word("sequence-01", df)
df['sequence-01'] = sequence01_f18
area_f19 = features.focus_word("area", df)
df['area'] = area_f19
soup_f20 = features.focus_word("soup", df)
df['soup'] = soup_f20
report01_f21 = features.focus_word("report-01", df)
df['report-01'] = report01_f21
head01_f22 = features.focus_word("head-01", df)
df['head-01'] = head01_f22
play01_f23 = features.focus_word("play-01", df)
df['play-01'] = play01_f23
status_f24 = features.focus_word("status", df)
df['status'] = status_f24
contact01_f25 = features.focus_word("contact-01", df)
df['contact-01'] = contact01_f25
deficiency_f26 = features.focus_word("deficiency", df)
df['deficiency'] = deficiency_f26
joy_f27 = features.focus_word("joy", df)
df['joy'] = joy_f27
thing_f28 = features.focus_word("thing", df)
df['thing'] = thing_f28
matter_f29 = features.focus_word("matter", df)
df['matter'] = matter_f29
certificate_f30 = features.focus_word("certificate", df)
df['certificate'] = certificate_f30
match03_f31 = features.focus_word("match-03", df)
df['match-03'] = match03_f31
consist01_f32 = features.focus_word("consist-01", df)
df['consist-01'] = consist01_f32
world_f33 = features.focus_word("world", df)
df['world'] = world_f33
work01_f34 = features.focus_word("work-01", df)
df['work-01'] = work01_f34
language_f35 = features.focus_word("language", df)
df['language'] = language_f35
degree_f36 = features.focus_word("degree", df)
df['degree'] = degree_f36
state_f37 = features.focus_word("state", df)
df['state'] = state_f37
place_f38 = features.focus_word("place", df)
df['place'] = place_f38
way_f39 = features.focus_word("way", df)
df['way'] = way_f39
interest_f40 = features.focus_word("interest", df)
df['interest'] = interest_f40
move01_41 = features.focus_word("move-01", df)
df['move-01'] = move01_41
train_f42 = features.focus_word("train", df)
df['train'] = train_f42
use01_f43 = features.focus_word("use-01", df)
df['use-01'] = use01_f43
surface_f44 = features.focus_word("surface", df)
df['surface'] = surface_f44
act02_f45 = features.focus_word("act-02", df)
df['act-02'] = act02_f45
lead03_f46 = features.focus_word("lead-03", df)
df['lead-03'] = lead03_f46
play11_f47 = features.focus_word("play-11", df)
df['play-11'] = play11_f47

poss_f48 = features.part_of_AMR(":poss", df)
df[':poss'] = poss_f48
part_f49 = features.part_of_AMR(":part ", df)
df[':part'] = part_f49
part_of_f50 = features.part_of_AMR(":part-of", df)
df[':part-of'] = part_of_f50
time_of_f51 = features.part_of_AMR(":time-of", df)
df[':time-of'] = time_of_f51
time_f52 = features.part_of_AMR(":time ", df)
df[':time'] = time_f52
source_f53 = features.part_of_AMR(":source", df)
df[':source'] = source_f53
polarity_f54 = features.part_of_AMR(":polarity", df)
df[':polarity'] = polarity_f54
domain_f55 = features.part_of_AMR(":domain", df)
df[':domain'] = domain_f55
topic_f56 = features.part_of_AMR(":topic", df)
df[':topic'] = topic_f56
location_of_f57 = features.part_of_AMR(":location-of", df)
df[':location-of'] = location_of_f57
location_f58 = features.part_of_AMR(":location ", df)
df[':location'] = location_f58
manner_f59 = features.part_of_AMR(":manner ", df)
df[':manner'] = manner_f59
manner_of_f60 = features.part_of_AMR(":manner-of", df)
df[':manner-of'] = manner_of_f60
purpose_f61 = features.part_of_AMR(":purpose", df)
df[':purpose'] = purpose_f61
have_rel_role91_f62 = features.part_of_AMR("have-rel-role-91", df)
df['have-rel-role-91'] = have_rel_role91_f62
ordinal_entity_f63 = features.part_of_AMR("ordinal-entity", df)
df['ordinal-entity'] = ordinal_entity_f63
accompanier_f64 = features.part_of_AMR(":accompanier", df)
df[':accompanier'] = accompanier_f64
value_f65 = features.part_of_AMR(":value", df)
df[':value'] = value_f65
date_entity_f66 = features.part_of_AMR("date-entity", df)
df['date-entity'] = date_entity_f66
date_interval_f67 = features.part_of_AMR("date-interval", df)
df['date-interval'] = date_interval_f67
consist_of_f68 = features.part_of_AMR(":consist-of", df)
df[':consist-of'] = consist_of_f68
instrument_f69 = features.part_of_AMR(":instrument", df)
df[':instrument'] = instrument_f69
cause01_f70 = features.part_of_AMR("cause-01", df)
df['cause-01'] = cause01_f70
medium_f71 = features.part_of_AMR(":medium", df)
df[':medium'] = medium_f71
name_f72 = features.part_of_AMR(":name", df)
df[':name'] = name_f72
include91_f73 = features.part_of_AMR("include-91", df)
df['include-91'] = include91_f73
have_org_role91_f74 = features.part_of_AMR("have-org-role-91", df)
df['have-org-role-91'] = have_org_role91_f74
type_f75 = features.part_of_AMR("type", df)
df['type'] = type_f75
man_f76 = features.part_of_AMR("man)", df)
df['man'] = man_f76
team_f77 = features.part_of_AMR("team", df)
df['team'] = team_f77
department_f78 = features.part_of_AMR("department", df)
df['department'] = department_f78
commission_f79 = features.part_of_AMR("commission", df)
df['commission'] = commission_f79
lead_80 = features.part_of_AMR("lead", df)
df['lead'] = lead_80
responsible_f81 = features.part_of_AMR("responsible", df)
df['responsible'] = responsible_f81
capable_f82 = features.part_of_AMR("capable", df)
df['capable'] = capable_f82
obtain_f83 = features.part_of_AMR("obtain", df)
df['obtain'] = obtain_f83
create_f84 = features.part_of_AMR("create", df)
df['create'] = create_f84
need_f85 = features.part_of_AMR("need", df)
df['need'] = need_f85

ARG0_f86 = features.first_role(":ARG0", df)
df[':ARG0'] = ARG0_f86
ARG1_f87 = features.first_role(":ARG1", df)
df[':ARG1'] = ARG1_f87
ARG2_f88 = features.first_role(":ARG2", df)
df[':ARG2'] = ARG2_f88
ARG3_f89 = features.first_role(":ARG3", df)
df[':ARG3'] = ARG3_f89
ARG0_of_f90 = features.first_role(":ARG0-of", df)
df[':ARG0-of'] = ARG0_of_f90
ARG1_of_f91 = features.first_role(":ARG1-of", df)
df[':ARG1-of'] = ARG1_of_f91
ARG2_of_f92 = features.first_role(":ARG2-of", df)
df[':ARG2-of'] = ARG2_of_f92
mod_f93 = features.first_role(":mod", df)
df[':mod'] = mod_f93

nodes_greater10_f94 = features.count_higher("/", 10, df)
df['nodes_count_11+'] = nodes_greater10_f94
nodes_less3_f95 = features.count_lower("/", 3, df)
df['nodes_count_2-'] = nodes_less3_f95
newlines_less3_f96 = features.count_lower("\n", 3, df)
df['newlines_count_2-'] = newlines_less3_f96
newlines_greater15_f97 = features.count_higher("\n", 15, df)
df['newlines_count_16+'] = newlines_greater15_f97

relation_in_AMR_f98 = features.relation_in_amr(df)
df['relation_in_AMR'] = relation_in_AMR_f98

end_bracket1_f99 = features.end_brackets("equal", 1, df)
df['one_bracket'] = end_bracket1_f99
end_brackets_greater5_f100 = features.end_brackets("greater", 5, df)
df['end_brackets_5+'] = end_brackets_greater5_f100

adj_greater1_f101 = features.POS_occurance("ADJ", 1, df)
df['adj_count_2+'] = adj_greater1_f101
verb_greater1_f102 = features.POS_occurance("VERB", 1, df)
df['verb_count_2+'] = verb_greater1_f102
adverb_greater0_f103 = features.POS_occurance("ADV", 0, df)
df['adverb_count_1+'] = adverb_greater0_f103

verb_firstPOS_f104 = features.first_POS("VERB", df)
df['verb_first_POS'] = verb_firstPOS_f104
noun_firstPOS_f105 = features.first_POS("NOUN", df)
df['noun_first_POS'] = noun_firstPOS_f105
propn_firstPOS_f106 = features.first_POS("PROPN", df)
df['propn_first_POS'] = propn_firstPOS_f106

df = df.drop('AMR', axis=1)
df.to_csv('amr_features_compound_relation.csv', sep=';', index=False)