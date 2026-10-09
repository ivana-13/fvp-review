# Summary for qwen3vl-32b

Gold check available: 409 of 933 checked actant-swap items have both actant boxes confirmed by Grounding DINO.

## actant-swap (933 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 884/933 (94.7%) |
| pairwise, order-debiased | 904/933 (96.9%) |
| blind pairwise (no image) | 807/933 (86.5%) |
| mean P(yes) caption / foil | 0.511 / 0.029 |
| yes-rate (P(yes)>0.5) caption / foil | 0.505 / 0.029 |

Verb naming: strict 265/933 (28.4%), WordNet-synonym 304/933 (32.6%)

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| agent | noun_prompt | 735/895 (82.1%) | 849/895 (94.9%) | 0.800 | 21 |
| agent | role_prompt | 718/895 (80.2%) | 838/895 (93.6%) | 0.784 | 16 |
| other-actant | noun_prompt | 704/971 (72.5%) | 881/971 (90.7%) | 0.698 | 34 |
| other-actant | role_prompt | 642/971 (66.1%) | 817/971 (84.1%) | 0.643 | 81 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 1866, full_image_box 0.311, image_center_point 0.671, largest_role_box 0.554, other_actant_box 0.107, random_box 0.020
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): n_targets 895, full_image_box 0.352, image_center_point 0.769, largest_role_box 0.639, other_actant_box 0.107, random_box 0.026
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 971, full_image_box 0.273, image_center_point 0.582, largest_role_box 0.475, other_actant_box 0.107, random_box 0.018

Both actants hit with role prompts, by role pair (top 8): agent-item 120/202; agent-victim 45/66; agent-vehicle 19/54; agent-target 20/52; agent-tool 25/48; agent-destination 5/38; agent-student 14/37; agent-contact 25/31

### Agreement, all items, foil outcome = pair_correct (n=933)

- pointing = both actants, role prompt: pointing hit 490/933 (52.5%); kappa(foil, pointing) = 0.033; cells {'foil+point+': 482, 'foil+point-': 422, 'foil-point+': 8, 'foil-point-': 21}
- pointing = agent only, role prompt: pointing hit 718/933 (77.0%); kappa(foil, pointing) = 0.020; cells {'foil+point+': 698, 'foil+point-': 206, 'foil-point+': 20, 'foil-point-': 9}
- pointing = both actants, noun prompt: pointing hit 562/933 (60.2%); kappa(foil, pointing) = 0.008; cells {'foil+point+': 546, 'foil+point-': 358, 'foil-point+': 16, 'foil-point-': 13}
- kappa(foil, blind) = 0.151; cells {'foil+point+': 793, 'foil+point-': 111, 'foil-point+': 14, 'foil-point-': 15}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+1.14, blind=+1.92; intercept=+1.56; fit acc 0.969 vs majority 0.969
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.45, blind=+1.80; intercept=+1.79; fit acc 0.969 vs majority 0.969

### Agreement, detector-verified gold only, foil outcome = pair_correct (n=409)

- pointing = both actants, role prompt: pointing hit 285/409 (69.7%); kappa(foil, pointing) = 0.073; cells {'foil+point+': 280, 'foil+point-': 115, 'foil-point+': 5, 'foil-point-': 9}
- pointing = agent only, role prompt: pointing hit 358/409 (87.5%); kappa(foil, pointing) = 0.008; cells {'foil+point+': 346, 'foil+point-': 49, 'foil-point+': 12, 'foil-point-': 2}
- pointing = both actants, noun prompt: pointing hit 364/409 (89.0%); kappa(foil, pointing) = -0.019; cells {'foil+point+': 351, 'foil+point-': 44, 'foil-point+': 13, 'foil-point-': 1}
- kappa(foil, blind) = 0.180; cells {'foil+point+': 346, 'foil+point-': 49, 'foil-point+': 6, 'foil-point-': 8}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+1.42, blind=+1.98; intercept=+1.06; fit acc 0.966 vs majority 0.966
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.22, blind=+1.72; intercept=+1.88; fit acc 0.966 vs majority 0.966

### Agreement, all items, foil outcome = yes_correct (n=933)

- pointing = both actants, role prompt: pointing hit 490/933 (52.5%); kappa(foil, pointing) = 0.026; cells {'foil+point+': 470, 'foil+point-': 414, 'foil-point+': 20, 'foil-point-': 29}
- pointing = agent only, role prompt: pointing hit 718/933 (77.0%); kappa(foil, pointing) = 0.064; cells {'foil+point+': 688, 'foil+point-': 196, 'foil-point+': 30, 'foil-point-': 19}
- pointing = both actants, noun prompt: pointing hit 562/933 (60.2%); kappa(foil, pointing) = 0.050; cells {'foil+point+': 542, 'foil+point-': 342, 'foil-point+': 20, 'foil-point-': 29}
- kappa(foil, blind) = 0.067; cells {'foil+point+': 770, 'foil+point-': 114, 'foil-point+': 37, 'foil-point-': 12}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.51, blind=+0.76; intercept=+2.02; fit acc 0.947 vs majority 0.947
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.76, blind=+0.74; intercept=+1.75; fit acc 0.947 vs majority 0.947

### Agreement, detector-verified gold only, foil outcome = yes_correct (n=409)

- pointing = both actants, role prompt: pointing hit 285/409 (69.7%); kappa(foil, pointing) = 0.013; cells {'foil+point+': 274, 'foil+point-': 118, 'foil-point+': 11, 'foil-point-': 6}
- pointing = agent only, role prompt: pointing hit 358/409 (87.5%); kappa(foil, pointing) = 0.028; cells {'foil+point+': 344, 'foil+point-': 48, 'foil-point+': 14, 'foil-point-': 3}
- pointing = both actants, noun prompt: pointing hit 364/409 (89.0%); kappa(foil, pointing) = 0.073; cells {'foil+point+': 351, 'foil+point-': 41, 'foil-point+': 13, 'foil-point-': 4}
- kappa(foil, blind) = 0.105; cells {'foil+point+': 341, 'foil+point-': 51, 'foil-point+': 11, 'foil-point-': 6}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.29, blind=+1.04; intercept=+2.11; fit acc 0.958 vs majority 0.958
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.36, blind=+1.03; intercept=+2.01; fit acc 0.958 vs majority 0.958

## action-replacement (630 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 579/630 (91.9%) |
| pairwise, order-debiased | 603/630 (95.7%) |
| blind pairwise (no image) | 414/630 (65.7%) |
| mean P(yes) caption / foil | 0.533 / 0.053 |

- agent pointing, role_prompt: IoU>=0.5 508/630 (80.6%), mean IoU 0.786
- agent pointing, noun_prompt: IoU>=0.5 502/630 (79.7%), mean IoU 0.769
- kappa(foil, agent pointing) = -0.032; cells {'foil+point+': 484, 'foil+point-': 119, 'foil-point+': 24, 'foil-point-': 3}
- kappa(foil, blind) = 0.087; cells {'foil+point+': 406, 'foil+point-': 197, 'foil-point+': 8, 'foil-point-': 19}
- logistic: foil_correct ~ pointing + blind: coef: pointing=-0.41, blind=+1.34; intercept=+2.77; fit acc 0.957 vs majority 0.957

## aro-relation (1228 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 1187/1228 (96.7%) |
| pairwise, order-debiased | 1196/1228 (97.4%) |
| blind pairwise (no image) | 1151/1228 (93.7%) |
| mean P(yes) caption / foil | 0.771 / 0.033 |
| yes-rate (P(yes)>0.5) caption / foil | 0.779 / 0.034 |
| pairwise on the benchmark crop | 1198/1228 (97.6%) |

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| other-actant | noun_prompt | 2173/2456 (88.5%) | 2330/2456 (94.9%) | 0.824 | 17 |
| other-actant | role_prompt | 1630/2456 (66.4%) | 1970/2456 (80.2%) | 0.644 | 55 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 2456, full_image_box 0.281, image_center_point 0.634, largest_role_box 0.601, other_actant_box 0.202, random_box 0.021
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): 
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 2456, full_image_box 0.281, image_center_point 0.634, largest_role_box 0.601, other_actant_box 0.202, random_box 0.021

Both actants hit with role prompts, by role pair (top 8): object-subject 581/1228

### Agreement, all items, foil outcome = pair_correct (n=1228)

- pointing = both actants, role prompt: pointing hit 581/1228 (47.3%); kappa(foil, pointing) = 0.035; cells {'foil+point+': 577, 'foil+point-': 619, 'foil-point+': 4, 'foil-point-': 28}
- pointing = agent only, role prompt: pointing hit 0/1228 (0.0%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 0, 'foil+point-': 1196, 'foil-point+': 0, 'foil-point-': 32}
- pointing = both actants, noun prompt: pointing hit 972/1228 (79.2%); kappa(foil, pointing) = 0.010; cells {'foil+point+': 948, 'foil+point-': 248, 'foil-point+': 24, 'foil-point-': 8}
- kappa(foil, blind) = 0.343; cells {'foil+point+': 1139, 'foil+point-': 57, 'foil-point+': 12, 'foil-point-': 20}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+1.49, blind=+3.05; intercept=+0.81; fit acc 0.974 vs majority 0.974
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+3.06; intercept=+1.26; fit acc 0.974 vs majority 0.974

### Agreement, all items, foil outcome = yes_correct (n=1228)

- pointing = both actants, role prompt: pointing hit 581/1228 (47.3%); kappa(foil, pointing) = 0.042; cells {'foil+point+': 575, 'foil+point-': 612, 'foil-point+': 6, 'foil-point-': 35}
- pointing = agent only, role prompt: pointing hit 0/1228 (0.0%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 0, 'foil+point-': 1187, 'foil-point+': 0, 'foil-point-': 41}
- pointing = both actants, noun prompt: pointing hit 972/1228 (79.2%); kappa(foil, pointing) = 0.018; cells {'foil+point+': 942, 'foil+point-': 245, 'foil-point+': 30, 'foil-point-': 11}
- kappa(foil, blind) = 0.273; cells {'foil+point+': 1128, 'foil+point-': 59, 'foil-point+': 23, 'foil-point-': 18}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+1.42, blind=+2.39; intercept=+0.94; fit acc 0.967 vs majority 0.967
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+2.42; intercept=+1.37; fit acc 0.967 vs majority 0.967

## aro-spatial (300 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 248/300 (82.7%) |
| pairwise, order-debiased | 251/300 (83.7%) |
| blind pairwise (no image) | 150/300 (50.0%) |
| mean P(yes) caption / foil | 0.432 / 0.027 |
| yes-rate (P(yes)>0.5) caption / foil | 0.433 / 0.030 |
| pairwise on the benchmark crop | 273/300 (91.0%) |

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| other-actant | noun_prompt | 449/600 (74.8%) | 508/600 (84.7%) | 0.687 | 13 |
| other-actant | role_prompt | 213/600 (35.5%) | 320/600 (53.3%) | 0.383 | 0 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 600, full_image_box 0.035, image_center_point 0.393, largest_role_box 0.500, other_actant_box 0.000, random_box 0.014
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): 
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 600, full_image_box 0.035, image_center_point 0.393, largest_role_box 0.500, other_actant_box 0.000, random_box 0.014

Both actants hit with role prompts, by role pair (top 8): object-subject 45/300

### Agreement, all items, foil outcome = pair_correct (n=300)

- pointing = both actants, role prompt: pointing hit 45/300 (15.0%); kappa(foil, pointing) = 0.003; cells {'foil+point+': 38, 'foil+point-': 213, 'foil-point+': 7, 'foil-point-': 42}
- pointing = agent only, role prompt: pointing hit 0/300 (0.0%); kappa(foil, pointing) = 0.000; cells {'foil+point+': 0, 'foil+point-': 251, 'foil-point+': 0, 'foil-point-': 49}
- pointing = both actants, noun prompt: pointing hit 172/300 (57.3%); kappa(foil, pointing) = 0.105; cells {'foil+point+': 151, 'foil+point-': 100, 'foil-point+': 21, 'foil-point-': 28}
- kappa(foil, blind) = 0.073; cells {'foil+point+': 131, 'foil+point-': 120, 'foil-point+': 19, 'foil-point-': 30}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.05, blind=+0.49; intercept=+1.40; fit acc 0.837 vs majority 0.837
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+0.49; intercept=+1.41; fit acc 0.837 vs majority 0.837

### Agreement, all items, foil outcome = yes_correct (n=300)

- pointing = both actants, role prompt: pointing hit 45/300 (15.0%); kappa(foil, pointing) = -0.011; cells {'foil+point+': 36, 'foil+point-': 212, 'foil-point+': 9, 'foil-point-': 43}
- pointing = agent only, role prompt: pointing hit 0/300 (0.0%); kappa(foil, pointing) = 0.000; cells {'foil+point+': 0, 'foil+point-': 248, 'foil-point+': 0, 'foil-point-': 52}
- pointing = both actants, noun prompt: pointing hit 172/300 (57.3%); kappa(foil, pointing) = 0.130; cells {'foil+point+': 151, 'foil+point-': 97, 'foil-point+': 21, 'foil-point-': 31}
- kappa(foil, blind) = 0.093; cells {'foil+point+': 131, 'foil+point-': 117, 'foil-point+': 19, 'foil-point-': 33}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=-0.19, blind=+0.61; intercept=+1.32; fit acc 0.827 vs majority 0.827
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+0.61; intercept=+1.29; fit acc 0.827 vs majority 0.827

## controls, actant-swap (933 items, 1866 role targets)

- text-only role resolution correct: 1764/1866 (94.5%) (agent 849/895 (94.9%), other 915/971 (94.2%))
- pointing hit, role prompt: unconditioned 1360/1866 (72.9%) | caption-conditioned 1428/1866 (76.5%) | noun prompt 1439/1866 (77.1%)
- caption-conditioned by target: agent 746/895 (83.4%), other 682/971 (70.2%)
- both participants by role: unconditioned 490/933 (52.5%) | conditioned 538/933 (57.7%)
- text resolved correctly but unconditioned pointing failed: 468/1764 (26.5%) of text-correct targets
- conflict pointing (foil caption in prompt), non-nested targets n=1666: image-consistent 856/1666 (51.4%), text-following 222/1666 (13.3%), both 13/1666 (0.8%), neither 575/1666 (34.5%); nested pairs excluded: 200

## controls, aro-relation (1228 items, 2456 role targets)

- text-only role resolution correct: 1985/2456 (80.8%) (agent n/a, other 1985/2456 (80.8%))
- pointing hit, role prompt: unconditioned 1624/2456 (66.1%) | caption-conditioned 2075/2456 (84.5%) | noun prompt 2173/2456 (88.5%)
- caption-conditioned by target: agent n/a, other 2075/2456 (84.5%)
- both participants by role: unconditioned 575/1228 (46.8%) | conditioned 890/1228 (72.5%)
- text resolved correctly but unconditioned pointing failed: 631/1985 (31.8%) of text-correct targets
- conflict pointing (foil caption in prompt), non-nested targets n=1960: image-consistent 793/1960 (40.5%), text-following 413/1960 (21.1%), both 24/1960 (1.2%), neither 730/1960 (37.2%); nested pairs excluded: 496

## blind likelihood baseline, actant-swap (933 items)

- caption more likely than foil (text only): 90.2% | clearly text-solvable (margin > 1.0 nat): 87.0% | balanced: 6.4% | foil preferred: 6.5%
- stratum solvable (n=812): foil pass 98.0%, both-by-role 52.1%, P(point | foil pass) 52.8%, cells {'foil+point+': 420, 'foil+point-': 376, 'foil-point+': 3, 'foil-point-': 13}
- stratum balanced (n=60): foil pass 91.7%, both-by-role 58.3%, P(point | foil pass) 56.4%, cells {'foil+point+': 31, 'foil+point-': 24, 'foil-point+': 4, 'foil-point-': 1}
- stratum foil_preferred (n=61): foil pass 86.9%, both-by-role 52.5%, P(point | foil pass) 58.5%, cells {'foil+point+': 31, 'foil+point-': 22, 'foil-point+': 1, 'foil-point-': 7}

## blind likelihood baseline, action-replacement (630 items)

- caption more likely than foil (text only): 71.6% | clearly text-solvable (margin > 1.0 nat): 65.7% | balanced: 12.1% | foil preferred: 22.2%

## blind likelihood baseline, aro-relation (1228 items)

- caption more likely than foil (text only): 94.7% | clearly text-solvable (margin > 1.0 nat): 92.1% | balanced: 5.5% | foil preferred: 2.4%
- stratum solvable (n=1134): foil pass 98.9%, both-by-role 48.1%, P(point | foil pass) 48.4%, cells {'foil+point+': 543, 'foil+point-': 579, 'foil-point+': 3, 'foil-point-': 9}
- stratum balanced (n=65): foil pass 80.0%, both-by-role 43.1%, P(point | foil pass) 51.9%, cells {'foil+point+': 27, 'foil+point-': 25, 'foil-point+': 1, 'foil-point-': 12}
- stratum foil_preferred (n=29): foil pass 75.9%, both-by-role 24.1%, P(point | foil pass) 31.8%, cells {'foil+point+': 7, 'foil+point-': 15, 'foil-point+': 0, 'foil-point-': 7}

## blind likelihood baseline, aro-spatial (300 items)

- caption more likely than foil (text only): 51.7% | clearly text-solvable (margin > 1.0 nat): 28.0% | balanced: 49.3% | foil preferred: 22.7%
- stratum solvable (n=84): foil pass 85.7%, both-by-role 16.7%, P(point | foil pass) 15.3%, cells {'foil+point+': 11, 'foil+point-': 61, 'foil-point+': 3, 'foil-point-': 9}
- stratum balanced (n=148): foil pass 81.8%, both-by-role 14.9%, P(point | foil pass) 14.9%, cells {'foil+point+': 18, 'foil+point-': 103, 'foil-point+': 4, 'foil-point-': 23}
- stratum foil_preferred (n=68): foil pass 85.3%, both-by-role 13.2%, P(point | foil pass) 15.5%, cells {'foil+point+': 9, 'foil+point-': 49, 'foil-point+': 0, 'foil-point-': 10}

