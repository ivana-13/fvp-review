# Summary for qwen3vl-8b

Gold check available: 409 of 933 checked actant-swap items have both actant boxes confirmed by Grounding DINO.

## actant-swap (933 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 830/933 (89.0%) |
| pairwise, order-debiased | 898/933 (96.2%) |
| blind pairwise (no image) | 40/933 (4.3%) |
| mean P(yes) caption / foil | 0.474 / 0.033 |
| yes-rate (P(yes)>0.5) caption / foil | 0.466 / 0.024 |

Verb naming: strict 250/933 (26.8%), WordNet-synonym 285/933 (30.5%)

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| agent | noun_prompt | 738/895 (82.5%) | 855/895 (95.5%) | 0.801 | 14 |
| agent | role_prompt | 693/895 (77.4%) | 817/895 (91.3%) | 0.756 | 34 |
| other-actant | noun_prompt | 709/971 (73.0%) | 889/971 (91.6%) | 0.699 | 23 |
| other-actant | role_prompt | 580/971 (59.7%) | 802/971 (82.6%) | 0.588 | 67 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 1866, full_image_box 0.311, image_center_point 0.671, largest_role_box 0.554, other_actant_box 0.107, random_box 0.020
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): n_targets 895, full_image_box 0.352, image_center_point 0.769, largest_role_box 0.639, other_actant_box 0.107, random_box 0.026
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 971, full_image_box 0.273, image_center_point 0.582, largest_role_box 0.475, other_actant_box 0.107, random_box 0.018

Both actants hit with role prompts, by role pair (top 8): agent-item 103/202; agent-victim 43/66; agent-vehicle 18/54; agent-target 18/52; agent-tool 17/48; agent-destination 4/38; agent-student 14/37; agent-contact 26/31

### Agreement, all items, foil outcome = pair_correct (n=933)

- pointing = both actants, role prompt: pointing hit 440/933 (47.2%); kappa(foil, pointing) = 0.022; cells {'foil+point+': 429, 'foil+point-': 469, 'foil-point+': 11, 'foil-point-': 24}
- pointing = agent only, role prompt: pointing hit 693/933 (74.3%); kappa(foil, pointing) = 0.031; cells {'foil+point+': 671, 'foil+point-': 227, 'foil-point+': 22, 'foil-point-': 13}
- pointing = both actants, noun prompt: pointing hit 568/933 (60.9%); kappa(foil, pointing) = 0.045; cells {'foil+point+': 555, 'foil+point-': 343, 'foil-point+': 13, 'foil-point-': 22}
- kappa(foil, blind) = -0.013; cells {'foil+point+': 33, 'foil+point-': 865, 'foil-point+': 7, 'foil-point-': 28}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.63, blind=-1.55; intercept=+3.12; fit acc 0.962 vs majority 0.962
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.50, blind=-1.54; intercept=+3.02; fit acc 0.962 vs majority 0.962

### Agreement, detector-verified gold only, foil outcome = pair_correct (n=409)

- pointing = both actants, role prompt: pointing hit 257/409 (62.8%); kappa(foil, pointing) = 0.033; cells {'foil+point+': 252, 'foil+point-': 145, 'foil-point+': 5, 'foil-point-': 7}
- pointing = agent only, role prompt: pointing hit 351/409 (85.8%); kappa(foil, pointing) = 0.009; cells {'foil+point+': 341, 'foil+point-': 56, 'foil-point+': 10, 'foil-point-': 2}
- pointing = both actants, noun prompt: pointing hit 363/409 (88.8%); kappa(foil, pointing) = 0.060; cells {'foil+point+': 354, 'foil+point-': 43, 'foil-point+': 9, 'foil-point-': 3}
- kappa(foil, blind) = -0.008; cells {'foil+point+': 13, 'foil+point-': 384, 'foil-point+': 2, 'foil-point-': 10}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.68, blind=-1.00; intercept=+3.18; fit acc 0.971 vs majority 0.971
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.12, blind=-0.94; intercept=+3.45; fit acc 0.971 vs majority 0.971

### Agreement, all items, foil outcome = yes_correct (n=933)

- pointing = both actants, role prompt: pointing hit 440/933 (47.2%); kappa(foil, pointing) = 0.068; cells {'foil+point+': 408, 'foil+point-': 422, 'foil-point+': 32, 'foil-point-': 71}
- pointing = agent only, role prompt: pointing hit 693/933 (74.3%); kappa(foil, pointing) = 0.066; cells {'foil+point+': 626, 'foil+point-': 204, 'foil-point+': 67, 'foil-point-': 36}
- pointing = both actants, noun prompt: pointing hit 568/933 (60.9%); kappa(foil, pointing) = 0.055; cells {'foil+point+': 516, 'foil+point-': 314, 'foil-point+': 52, 'foil-point-': 51}
- kappa(foil, blind) = -0.016; cells {'foil+point+': 29, 'foil+point-': 801, 'foil-point+': 11, 'foil-point-': 92}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.74, blind=-1.08; intercept=+1.86; fit acc 0.890 vs majority 0.890
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.48, blind=-1.06; intercept=+1.81; fit acc 0.890 vs majority 0.890

### Agreement, detector-verified gold only, foil outcome = yes_correct (n=409)

- pointing = both actants, role prompt: pointing hit 257/409 (62.8%); kappa(foil, pointing) = 0.106; cells {'foil+point+': 238, 'foil+point-': 127, 'foil-point+': 19, 'foil-point-': 25}
- pointing = agent only, role prompt: pointing hit 351/409 (85.8%); kappa(foil, pointing) = 0.039; cells {'foil+point+': 315, 'foil+point-': 50, 'foil-point+': 36, 'foil-point-': 8}
- pointing = both actants, noun prompt: pointing hit 363/409 (88.8%); kappa(foil, pointing) = 0.001; cells {'foil+point+': 324, 'foil+point-': 41, 'foil-point+': 39, 'foil-point-': 5}
- kappa(foil, blind) = -0.019; cells {'foil+point+': 10, 'foil+point-': 355, 'foil-point+': 5, 'foil-point-': 39}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.85, blind=-1.22; intercept=+1.71; fit acc 0.892 vs majority 0.892
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.29, blind=-1.13; intercept=+1.93; fit acc 0.892 vs majority 0.892

## action-replacement (630 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 576/630 (91.4%) |
| pairwise, order-debiased | 601/630 (95.4%) |
| blind pairwise (no image) | 171/630 (27.1%) |
| mean P(yes) caption / foil | 0.479 / 0.043 |

- agent pointing, role_prompt: IoU>=0.5 488/630 (77.5%), mean IoU 0.757
- agent pointing, noun_prompt: IoU>=0.5 502/630 (79.7%), mean IoU 0.767
- kappa(foil, agent pointing) = 0.057; cells {'foil+point+': 470, 'foil+point-': 131, 'foil-point+': 18, 'foil-point-': 11}
- kappa(foil, blind) = -0.010; cells {'foil+point+': 161, 'foil+point-': 440, 'foil-point+': 10, 'foil-point-': 19}
- logistic: foil_correct ~ pointing + blind: coef: pointing=+0.68, blind=-0.31; intercept=+2.64; fit acc 0.954 vs majority 0.954

## aro-relation (1228 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 1157/1228 (94.2%) |
| pairwise, order-debiased | 1181/1228 (96.2%) |
| blind pairwise (no image) | 45/1228 (3.7%) |
| mean P(yes) caption / foil | 0.778 / 0.051 |
| yes-rate (P(yes)>0.5) caption / foil | 0.782 / 0.048 |
| pairwise on the benchmark crop | 1191/1228 (97.0%) |

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| other-actant | noun_prompt | 2170/2456 (88.4%) | 2333/2456 (95.0%) | 0.821 | 7 |
| other-actant | role_prompt | 1515/2456 (61.7%) | 1954/2456 (79.6%) | 0.599 | 0 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 2456, full_image_box 0.281, image_center_point 0.634, largest_role_box 0.601, other_actant_box 0.202, random_box 0.021
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): 
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 2456, full_image_box 0.281, image_center_point 0.634, largest_role_box 0.601, other_actant_box 0.202, random_box 0.021

Both actants hit with role prompts, by role pair (top 8): object-subject 515/1228

### Agreement, all items, foil outcome = pair_correct (n=1228)

- pointing = both actants, role prompt: pointing hit 515/1228 (41.9%); kappa(foil, pointing) = 0.036; cells {'foil+point+': 508, 'foil+point-': 673, 'foil-point+': 7, 'foil-point-': 40}
- pointing = agent only, role prompt: pointing hit 0/1228 (0.0%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 0, 'foil+point-': 1181, 'foil-point+': 0, 'foil-point-': 47}
- pointing = both actants, noun prompt: pointing hit 972/1228 (79.2%); kappa(foil, pointing) = 0.016; cells {'foil+point+': 937, 'foil+point-': 244, 'foil-point+': 35, 'foil-point-': 12}
- kappa(foil, blind) = -0.018; cells {'foil+point+': 33, 'foil+point-': 1148, 'foil-point+': 12, 'foil-point-': 35}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+1.11, blind=-1.95; intercept=+3.09; fit acc 0.962 vs majority 0.962
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=-2.16; intercept=+3.43; fit acc 0.962 vs majority 0.962

### Agreement, all items, foil outcome = yes_correct (n=1228)

- pointing = both actants, role prompt: pointing hit 515/1228 (41.9%); kappa(foil, pointing) = 0.048; cells {'foil+point+': 502, 'foil+point-': 655, 'foil-point+': 13, 'foil-point-': 58}
- pointing = agent only, role prompt: pointing hit 0/1228 (0.0%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 0, 'foil+point-': 1157, 'foil-point+': 0, 'foil-point-': 71}
- pointing = both actants, noun prompt: pointing hit 972/1228 (79.2%); kappa(foil, pointing) = 0.069; cells {'foil+point+': 926, 'foil+point-': 231, 'foil-point+': 46, 'foil-point-': 25}
- kappa(foil, blind) = -0.020; cells {'foil+point+': 31, 'foil+point-': 1126, 'foil-point+': 14, 'foil-point-': 57}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+1.00, blind=-1.75; intercept=+2.62; fit acc 0.942 vs majority 0.942
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=-1.94; intercept=+2.95; fit acc 0.942 vs majority 0.942

## aro-spatial (300 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 245/300 (81.7%) |
| pairwise, order-debiased | 245/300 (81.7%) |
| blind pairwise (no image) | 135/300 (45.0%) |
| mean P(yes) caption / foil | 0.521 / 0.074 |
| yes-rate (P(yes)>0.5) caption / foil | 0.520 / 0.057 |
| pairwise on the benchmark crop | 272/300 (90.7%) |

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| other-actant | noun_prompt | 428/600 (71.3%) | 494/600 (82.3%) | 0.675 | 8 |
| other-actant | role_prompt | 108/600 (18.0%) | 212/600 (35.3%) | 0.217 | 0 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 600, full_image_box 0.035, image_center_point 0.393, largest_role_box 0.500, other_actant_box 0.000, random_box 0.014
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): 
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 600, full_image_box 0.035, image_center_point 0.393, largest_role_box 0.500, other_actant_box 0.000, random_box 0.014

Both actants hit with role prompts, by role pair (top 8): object-subject 3/300

### Agreement, all items, foil outcome = pair_correct (n=300)

- pointing = both actants, role prompt: pointing hit 3/300 (1.0%); kappa(foil, pointing) = -0.004; cells {'foil+point+': 2, 'foil+point-': 243, 'foil-point+': 1, 'foil-point-': 54}
- pointing = agent only, role prompt: pointing hit 0/300 (0.0%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 0, 'foil+point-': 245, 'foil-point+': 0, 'foil-point-': 55}
- pointing = both actants, noun prompt: pointing hit 156/300 (52.0%); kappa(foil, pointing) = 0.090; cells {'foil+point+': 134, 'foil+point-': 111, 'foil-point+': 22, 'foil-point-': 33}
- kappa(foil, blind) = 0.085; cells {'foil+point+': 117, 'foil+point-': 128, 'foil-point+': 18, 'foil-point-': 37}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=-0.35, blind=+0.58; intercept=+1.26; fit acc 0.817 vs majority 0.817
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+0.57; intercept=+1.26; fit acc 0.817 vs majority 0.817

### Agreement, all items, foil outcome = yes_correct (n=300)

- pointing = both actants, role prompt: pointing hit 3/300 (1.0%); kappa(foil, pointing) = -0.004; cells {'foil+point+': 2, 'foil+point-': 243, 'foil-point+': 1, 'foil-point-': 54}
- pointing = agent only, role prompt: pointing hit 0/300 (0.0%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 0, 'foil+point-': 245, 'foil-point+': 0, 'foil-point-': 55}
- pointing = both actants, noun prompt: pointing hit 156/300 (52.0%); kappa(foil, pointing) = 0.118; cells {'foil+point+': 136, 'foil+point-': 109, 'foil-point+': 20, 'foil-point-': 35}
- kappa(foil, blind) = 0.097; cells {'foil+point+': 118, 'foil+point-': 127, 'foil-point+': 17, 'foil-point-': 38}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=-0.36, blind=+0.67; intercept=+1.23; fit acc 0.817 vs majority 0.817
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+0.66; intercept=+1.23; fit acc 0.817 vs majority 0.817

## controls, actant-swap (933 items, 1866 role targets)

- text-only role resolution correct: 1725/1866 (92.4%) (agent 844/895 (94.3%), other 881/971 (90.7%))
- pointing hit, role prompt: unconditioned 1273/1866 (68.2%) | caption-conditioned 1370/1866 (73.4%) | noun prompt 1447/1866 (77.5%)
- caption-conditioned by target: agent 738/895 (82.5%), other 632/971 (65.1%)
- both participants by role: unconditioned 440/933 (47.2%) | conditioned 498/933 (53.4%)
- text resolved correctly but unconditioned pointing failed: 545/1725 (31.6%) of text-correct targets
- conflict pointing (foil caption in prompt), non-nested targets n=1666: image-consistent 940/1666 (56.4%), text-following 264/1666 (15.8%), both 11/1666 (0.7%), neither 451/1666 (27.1%); nested pairs excluded: 200

## controls, aro-relation (1228 items, 2456 role targets)

- text-only role resolution correct: 2106/2456 (85.7%) (agent n/a, other 2106/2456 (85.7%))
- pointing hit, role prompt: unconditioned 1513/2456 (61.6%) | caption-conditioned 1916/2456 (78.0%) | noun prompt 2170/2456 (88.4%)
- caption-conditioned by target: agent n/a, other 1916/2456 (78.0%)
- both participants by role: unconditioned 510/1228 (41.5%) | conditioned 770/1228 (62.7%)
- text resolved correctly but unconditioned pointing failed: 762/2106 (36.2%) of text-correct targets
- conflict pointing (foil caption in prompt), non-nested targets n=1960: image-consistent 1180/1960 (60.2%), text-following 441/1960 (22.5%), both 35/1960 (1.8%), neither 304/1960 (15.5%); nested pairs excluded: 496

## blind likelihood baseline, actant-swap (933 items)

- caption more likely than foil (text only): 90.0% | clearly text-solvable (margin > 1.0 nat): 85.0% | balanced: 7.7% | foil preferred: 7.3%
- stratum solvable (n=793): foil pass 97.2%, both-by-role 47.0%, P(point | foil pass) 47.9%, cells {'foil+point+': 369, 'foil+point-': 402, 'foil-point+': 4, 'foil-point-': 18}
- stratum balanced (n=72): foil pass 94.4%, both-by-role 45.8%, P(point | foil pass) 44.1%, cells {'foil+point+': 30, 'foil+point-': 38, 'foil-point+': 3, 'foil-point-': 1}
- stratum foil_preferred (n=68): foil pass 86.8%, both-by-role 50.0%, P(point | foil pass) 50.8%, cells {'foil+point+': 30, 'foil+point-': 29, 'foil-point+': 4, 'foil-point-': 5}

## blind likelihood baseline, action-replacement (630 items)

- caption more likely than foil (text only): 69.8% | clearly text-solvable (margin > 1.0 nat): 62.2% | balanced: 14.1% | foil preferred: 23.7%

## blind likelihood baseline, aro-relation (1228 items)

- caption more likely than foil (text only): 96.3% | clearly text-solvable (margin > 1.0 nat): 93.0% | balanced: 5.1% | foil preferred: 1.9%
- stratum solvable (n=1144): foil pass 98.0%, both-by-role 43.4%, P(point | foil pass) 43.9%, cells {'foil+point+': 492, 'foil+point-': 629, 'foil-point+': 4, 'foil-point-': 19}
- stratum balanced (n=62): foil pass 75.8%, both-by-role 24.2%, P(point | foil pass) 27.7%, cells {'foil+point+': 13, 'foil+point-': 34, 'foil-point+': 2, 'foil-point-': 13}
- stratum foil_preferred (n=22): foil pass 59.1%, both-by-role 18.2%, P(point | foil pass) 23.1%, cells {'foil+point+': 3, 'foil+point-': 10, 'foil-point+': 1, 'foil-point-': 8}

## blind likelihood baseline, aro-spatial (300 items)

- caption more likely than foil (text only): 48.3% | clearly text-solvable (margin > 1.0 nat): 31.3% | balanced: 35.3% | foil preferred: 33.3%
- stratum solvable (n=94): foil pass 89.4%, both-by-role 1.1%, P(point | foil pass) 1.2%, cells {'foil+point+': 1, 'foil+point-': 83, 'foil-point+': 0, 'foil-point-': 10}
- stratum balanced (n=106): foil pass 82.1%, both-by-role 0.0%, P(point | foil pass) 0.0%, cells {'foil+point+': 0, 'foil+point-': 87, 'foil-point+': 0, 'foil-point-': 19}
- stratum foil_preferred (n=100): foil pass 74.0%, both-by-role 2.0%, P(point | foil pass) 1.4%, cells {'foil+point+': 1, 'foil+point-': 73, 'foil-point+': 1, 'foil-point-': 25}

