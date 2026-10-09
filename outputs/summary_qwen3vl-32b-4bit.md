# Summary for qwen3vl-32b-4bit

Gold check available: 409 of 933 checked actant-swap items have both actant boxes confirmed by Grounding DINO.

## actant-swap (933 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 876/933 (93.9%) |
| pairwise, order-debiased | 908/933 (97.3%) |
| blind pairwise (no image) | 729/933 (78.1%) |
| mean P(yes) caption / foil | 0.508 / 0.026 |
| yes-rate (P(yes)>0.5) caption / foil | 0.504 / 0.024 |

Verb naming: strict 264/933 (28.3%), WordNet-synonym 303/933 (32.5%)

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| agent | noun_prompt | 733/895 (81.9%) | 845/895 (94.4%) | 0.795 | 21 |
| agent | role_prompt | 717/895 (80.1%) | 839/895 (93.7%) | 0.783 | 16 |
| other-actant | noun_prompt | 705/971 (72.6%) | 883/971 (90.9%) | 0.698 | 33 |
| other-actant | role_prompt | 634/971 (65.3%) | 804/971 (82.8%) | 0.630 | 100 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 1866, full_image_box 0.311, image_center_point 0.671, largest_role_box 0.554, other_actant_box 0.107, random_box 0.020
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): n_targets 895, full_image_box 0.352, image_center_point 0.769, largest_role_box 0.639, other_actant_box 0.107, random_box 0.026
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 971, full_image_box 0.273, image_center_point 0.582, largest_role_box 0.475, other_actant_box 0.107, random_box 0.018

Both actants hit with role prompts, by role pair (top 8): agent-item 123/202; agent-victim 46/66; agent-vehicle 18/54; agent-target 19/52; agent-tool 25/48; agent-destination 4/38; agent-student 14/37; agent-contact 24/31

### Agreement, all items, foil outcome = pair_correct (n=933)

- pointing = both actants, role prompt: pointing hit 483/933 (51.8%); kappa(foil, pointing) = 0.026; cells {'foil+point+': 476, 'foil+point-': 432, 'foil-point+': 7, 'foil-point-': 18}
- pointing = agent only, role prompt: pointing hit 717/933 (76.8%); kappa(foil, pointing) = 0.011; cells {'foil+point+': 699, 'foil+point-': 209, 'foil-point+': 18, 'foil-point-': 7}
- pointing = both actants, noun prompt: pointing hit 560/933 (60.0%); kappa(foil, pointing) = 0.011; cells {'foil+point+': 547, 'foil+point-': 361, 'foil-point+': 13, 'foil-point-': 12}
- kappa(foil, blind) = 0.115; cells {'foil+point+': 722, 'foil+point-': 186, 'foil-point+': 7, 'foil-point-': 18}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+1.04, blind=+2.03; intercept=+1.96; fit acc 0.973 vs majority 0.973
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.38, blind=+1.96; intercept=+2.16; fit acc 0.973 vs majority 0.973

### Agreement, detector-verified gold only, foil outcome = pair_correct (n=409)

- pointing = both actants, role prompt: pointing hit 283/409 (69.2%); kappa(foil, pointing) = 0.055; cells {'foil+point+': 279, 'foil+point-': 119, 'foil-point+': 4, 'foil-point-': 7}
- pointing = agent only, role prompt: pointing hit 357/409 (87.3%); kappa(foil, pointing) = 0.020; cells {'foil+point+': 348, 'foil+point-': 50, 'foil-point+': 9, 'foil-point-': 2}
- pointing = both actants, noun prompt: pointing hit 360/409 (88.0%); kappa(foil, pointing) = -0.011; cells {'foil+point+': 350, 'foil+point-': 48, 'foil-point+': 10, 'foil-point-': 1}
- kappa(foil, blind) = 0.123; cells {'foil+point+': 320, 'foil+point-': 78, 'foil-point+': 3, 'foil-point-': 8}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+1.22, blind=+1.84; intercept=+1.72; fit acc 0.973 vs majority 0.973
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.38, blind=+1.71; intercept=+2.19; fit acc 0.973 vs majority 0.973

### Agreement, all items, foil outcome = yes_correct (n=933)

- pointing = both actants, role prompt: pointing hit 483/933 (51.8%); kappa(foil, pointing) = 0.033; cells {'foil+point+': 461, 'foil+point-': 415, 'foil-point+': 22, 'foil-point-': 35}
- pointing = agent only, role prompt: pointing hit 717/933 (76.8%); kappa(foil, pointing) = 0.071; cells {'foil+point+': 682, 'foil+point-': 194, 'foil-point+': 35, 'foil-point-': 22}
- pointing = both actants, noun prompt: pointing hit 560/933 (60.0%); kappa(foil, pointing) = 0.058; cells {'foil+point+': 537, 'foil+point-': 339, 'foil-point+': 23, 'foil-point-': 34}
- kappa(foil, blind) = -0.004; cells {'foil+point+': 684, 'foil+point-': 192, 'foil-point+': 45, 'foil-point-': 12}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.53, blind=-0.00; intercept=+2.49; fit acc 0.939 vs majority 0.939
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.74, blind=+0.00; intercept=+2.21; fit acc 0.939 vs majority 0.939

### Agreement, detector-verified gold only, foil outcome = yes_correct (n=409)

- pointing = both actants, role prompt: pointing hit 283/409 (69.2%); kappa(foil, pointing) = 0.017; cells {'foil+point+': 271, 'foil+point-': 119, 'foil-point+': 12, 'foil-point-': 7}
- pointing = agent only, role prompt: pointing hit 357/409 (87.3%); kappa(foil, pointing) = 0.048; cells {'foil+point+': 342, 'foil+point-': 48, 'foil-point+': 15, 'foil-point-': 4}
- pointing = both actants, noun prompt: pointing hit 360/409 (88.0%); kappa(foil, pointing) = 0.054; cells {'foil+point+': 345, 'foil+point-': 45, 'foil-point+': 15, 'foil-point-': 4}
- kappa(foil, blind) = 0.021; cells {'foil+point+': 309, 'foil+point-': 81, 'foil-point+': 14, 'foil-point-': 5}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.24, blind=+0.27; intercept=+2.65; fit acc 0.954 vs majority 0.954
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.49, blind=+0.27; intercept=+2.40; fit acc 0.954 vs majority 0.954

## action-replacement (630 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 583/630 (92.5%) |
| pairwise, order-debiased | 602/630 (95.6%) |
| blind pairwise (no image) | 387/630 (61.4%) |
| mean P(yes) caption / foil | 0.528 / 0.054 |

- agent pointing, role_prompt: IoU>=0.5 508/630 (80.6%), mean IoU 0.783
- agent pointing, noun_prompt: IoU>=0.5 504/630 (80.0%), mean IoU 0.768
- kappa(foil, agent pointing) = -0.020; cells {'foil+point+': 484, 'foil+point-': 118, 'foil-point+': 24, 'foil-point-': 4}
- kappa(foil, blind) = 0.058; cells {'foil+point+': 377, 'foil+point-': 225, 'foil-point+': 10, 'foil-point-': 18}
- logistic: foil_correct ~ pointing + blind: coef: pointing=-0.25, blind=+0.94; intercept=+2.79; fit acc 0.956 vs majority 0.956

## aro-relation (1228 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 1183/1228 (96.3%) |
| pairwise, order-debiased | 1199/1228 (97.6%) |
| blind pairwise (no image) | 1042/1228 (84.9%) |
| mean P(yes) caption / foil | 0.756 / 0.032 |
| yes-rate (P(yes)>0.5) caption / foil | 0.759 / 0.033 |
| pairwise on the benchmark crop | 1200/1228 (97.7%) |

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| other-actant | noun_prompt | 2164/2456 (88.1%) | 2321/2456 (94.5%) | 0.819 | 19 |
| other-actant | role_prompt | 1641/2456 (66.8%) | 1980/2456 (80.6%) | 0.646 | 50 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 2456, full_image_box 0.281, image_center_point 0.634, largest_role_box 0.601, other_actant_box 0.202, random_box 0.021
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): 
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 2456, full_image_box 0.281, image_center_point 0.634, largest_role_box 0.601, other_actant_box 0.202, random_box 0.021

Both actants hit with role prompts, by role pair (top 8): object-subject 595/1228

### Agreement, all items, foil outcome = pair_correct (n=1228)

- pointing = both actants, role prompt: pointing hit 595/1228 (48.5%); kappa(foil, pointing) = 0.041; cells {'foil+point+': 594, 'foil+point-': 605, 'foil-point+': 1, 'foil-point-': 28}
- pointing = agent only, role prompt: pointing hit 0/1228 (0.0%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 0, 'foil+point-': 1199, 'foil-point+': 0, 'foil-point-': 29}
- pointing = both actants, noun prompt: pointing hit 964/1228 (78.5%); kappa(foil, pointing) = 0.005; cells {'foil+point+': 942, 'foil+point-': 257, 'foil-point+': 22, 'foil-point-': 7}
- kappa(foil, blind) = 0.122; cells {'foil+point+': 1030, 'foil+point-': 169, 'foil-point+': 12, 'foil-point-': 17}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+2.08, blind=+1.86; intercept=+1.87; fit acc 0.976 vs majority 0.976
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+1.88; intercept=+2.43; fit acc 0.976 vs majority 0.976

### Agreement, all items, foil outcome = yes_correct (n=1228)

- pointing = both actants, role prompt: pointing hit 595/1228 (48.5%); kappa(foil, pointing) = 0.047; cells {'foil+point+': 588, 'foil+point-': 595, 'foil-point+': 7, 'foil-point-': 38}
- pointing = agent only, role prompt: pointing hit 0/1228 (0.0%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 0, 'foil+point-': 1183, 'foil-point+': 0, 'foil-point-': 45}
- pointing = both actants, noun prompt: pointing hit 964/1228 (78.5%); kappa(foil, pointing) = 0.016; cells {'foil+point+': 931, 'foil+point-': 252, 'foil-point+': 33, 'foil-point-': 12}
- kappa(foil, blind) = 0.103; cells {'foil+point+': 1015, 'foil+point-': 168, 'foil-point+': 27, 'foil-point-': 18}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+1.43, blind=+1.24; intercept=+1.87; fit acc 0.963 vs majority 0.963
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+1.27; intercept=+2.31; fit acc 0.963 vs majority 0.963

## aro-spatial (300 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 244/300 (81.3%) |
| pairwise, order-debiased | 252/300 (84.0%) |
| blind pairwise (no image) | 150/300 (50.0%) |
| mean P(yes) caption / foil | 0.400 / 0.019 |
| yes-rate (P(yes)>0.5) caption / foil | 0.403 / 0.017 |
| pairwise on the benchmark crop | 273/300 (91.0%) |

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| other-actant | noun_prompt | 443/600 (73.8%) | 499/600 (83.2%) | 0.680 | 18 |
| other-actant | role_prompt | 200/600 (33.3%) | 314/600 (52.3%) | 0.370 | 0 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 600, full_image_box 0.035, image_center_point 0.393, largest_role_box 0.500, other_actant_box 0.000, random_box 0.014
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): 
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 600, full_image_box 0.035, image_center_point 0.393, largest_role_box 0.500, other_actant_box 0.000, random_box 0.014

Both actants hit with role prompts, by role pair (top 8): object-subject 38/300

### Agreement, all items, foil outcome = pair_correct (n=300)

- pointing = both actants, role prompt: pointing hit 38/300 (12.7%); kappa(foil, pointing) = -0.008; cells {'foil+point+': 31, 'foil+point-': 221, 'foil-point+': 7, 'foil-point-': 41}
- pointing = agent only, role prompt: pointing hit 0/300 (0.0%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 0, 'foil+point-': 252, 'foil-point+': 0, 'foil-point-': 48}
- pointing = both actants, noun prompt: pointing hit 171/300 (57.0%); kappa(foil, pointing) = 0.108; cells {'foil+point+': 151, 'foil+point-': 101, 'foil-point+': 20, 'foil-point-': 28}
- kappa(foil, blind) = 0.067; cells {'foil+point+': 131, 'foil+point-': 121, 'foil-point+': 19, 'foil-point-': 29}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=-0.18, blind=+0.46; intercept=+1.47; fit acc 0.840 vs majority 0.840
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+0.46; intercept=+1.45; fit acc 0.840 vs majority 0.840

### Agreement, all items, foil outcome = yes_correct (n=300)

- pointing = both actants, role prompt: pointing hit 38/300 (12.7%); kappa(foil, pointing) = -0.008; cells {'foil+point+': 30, 'foil+point-': 214, 'foil-point+': 8, 'foil-point-': 48}
- pointing = agent only, role prompt: pointing hit 0/300 (0.0%); kappa(foil, pointing) = 0.000; cells {'foil+point+': 0, 'foil+point-': 244, 'foil-point+': 0, 'foil-point-': 56}
- pointing = both actants, noun prompt: pointing hit 171/300 (57.0%); kappa(foil, pointing) = 0.145; cells {'foil+point+': 149, 'foil+point-': 95, 'foil-point+': 22, 'foil-point-': 34}
- kappa(foil, blind) = 0.093; cells {'foil+point+': 129, 'foil+point-': 115, 'foil-point+': 21, 'foil-point-': 35}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=-0.16, blind=+0.57; intercept=+1.23; fit acc 0.813 vs majority 0.813
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+0.57; intercept=+1.21; fit acc 0.813 vs majority 0.813

## controls, actant-swap (933 items, 1866 role targets)

- text-only role resolution correct: 1758/1866 (94.2%) (agent 849/895 (94.9%), other 909/971 (93.6%))
- pointing hit, role prompt: unconditioned 1351/1866 (72.4%) | caption-conditioned 1433/1866 (76.8%) | noun prompt 1438/1866 (77.1%)
- caption-conditioned by target: agent 748/895 (83.6%), other 685/971 (70.5%)
- both participants by role: unconditioned 483/933 (51.8%) | conditioned 542/933 (58.1%)
- text resolved correctly but unconditioned pointing failed: 470/1758 (26.7%) of text-correct targets
- conflict pointing (foil caption in prompt), non-nested targets n=1666: image-consistent 896/1666 (53.8%), text-following 250/1666 (15.0%), both 10/1666 (0.6%), neither 510/1666 (30.6%); nested pairs excluded: 200

## controls, aro-relation (1228 items, 2456 role targets)

- text-only role resolution correct: 1959/2456 (79.8%) (agent n/a, other 1959/2456 (79.8%))
- pointing hit, role prompt: unconditioned 1646/2456 (67.0%) | caption-conditioned 2042/2456 (83.1%) | noun prompt 2164/2456 (88.1%)
- caption-conditioned by target: agent n/a, other 2042/2456 (83.1%)
- both participants by role: unconditioned 598/1228 (48.7%) | conditioned 868/1228 (70.7%)
- text resolved correctly but unconditioned pointing failed: 611/1959 (31.2%) of text-correct targets
- conflict pointing (foil caption in prompt), non-nested targets n=1960: image-consistent 888/1960 (45.3%), text-following 421/1960 (21.5%), both 27/1960 (1.4%), neither 624/1960 (31.8%); nested pairs excluded: 496

## blind likelihood baseline, actant-swap (933 items)

- caption more likely than foil (text only): 89.8% | clearly text-solvable (margin > 1.0 nat): 86.4% | balanced: 7.0% | foil preferred: 6.6%
- stratum solvable (n=806): foil pass 98.5%, both-by-role 51.2%, P(point | foil pass) 51.6%, cells {'foil+point+': 410, 'foil+point-': 384, 'foil-point+': 3, 'foil-point-': 9}
- stratum balanced (n=65): foil pass 90.8%, both-by-role 53.8%, P(point | foil pass) 54.2%, cells {'foil+point+': 32, 'foil+point-': 27, 'foil-point+': 3, 'foil-point-': 3}
- stratum foil_preferred (n=62): foil pass 88.7%, both-by-role 56.5%, P(point | foil pass) 61.8%, cells {'foil+point+': 34, 'foil+point-': 21, 'foil-point+': 1, 'foil-point-': 6}

## blind likelihood baseline, action-replacement (630 items)

- caption more likely than foil (text only): 71.1% | clearly text-solvable (margin > 1.0 nat): 65.1% | balanced: 12.7% | foil preferred: 22.2%

## blind likelihood baseline, aro-relation (1228 items)

- caption more likely than foil (text only): 95.5% | clearly text-solvable (margin > 1.0 nat): 90.0% | balanced: 7.6% | foil preferred: 2.4%
- stratum solvable (n=1109): foil pass 99.0%, both-by-role 49.9%, P(point | foil pass) 50.4%, cells {'foil+point+': 553, 'foil+point-': 545, 'foil-point+': 0, 'foil-point-': 11}
- stratum balanced (n=90): foil pass 87.8%, both-by-role 40.0%, P(point | foil pass) 44.3%, cells {'foil+point+': 35, 'foil+point-': 44, 'foil-point+': 1, 'foil-point-': 10}
- stratum foil_preferred (n=29): foil pass 75.9%, both-by-role 20.7%, P(point | foil pass) 27.3%, cells {'foil+point+': 6, 'foil+point-': 16, 'foil-point+': 0, 'foil-point-': 7}

## blind likelihood baseline, aro-spatial (300 items)

- caption more likely than foil (text only): 49.0% | clearly text-solvable (margin > 1.0 nat): 30.3% | balanced: 44.0% | foil preferred: 25.7%
- stratum solvable (n=91): foil pass 85.7%, both-by-role 8.8%, P(point | foil pass) 6.4%, cells {'foil+point+': 5, 'foil+point-': 73, 'foil-point+': 3, 'foil-point-': 10}
- stratum balanced (n=132): foil pass 80.3%, both-by-role 16.7%, P(point | foil pass) 17.0%, cells {'foil+point+': 18, 'foil+point-': 88, 'foil-point+': 4, 'foil-point-': 22}
- stratum foil_preferred (n=77): foil pass 88.3%, both-by-role 10.4%, P(point | foil pass) 11.8%, cells {'foil+point+': 8, 'foil+point-': 60, 'foil-point+': 0, 'foil-point-': 9}

