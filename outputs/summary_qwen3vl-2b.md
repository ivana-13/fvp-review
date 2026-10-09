# Summary for qwen3vl-2b

Gold check available: 409 of 933 checked actant-swap items have both actant boxes confirmed by Grounding DINO.

## actant-swap (933 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 742/933 (79.5%) |
| pairwise, order-debiased | 866/933 (92.8%) |
| blind pairwise (no image) | 483/933 (51.8%) |
| mean P(yes) caption / foil | 0.628 / 0.298 |
| yes-rate (P(yes)>0.5) caption / foil | 0.635 / 0.282 |

Verb naming: strict 192/933 (20.6%), WordNet-synonym 219/933 (23.5%)

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| agent | noun_prompt | 714/895 (79.8%) | 834/895 (93.2%) | 0.771 | 18 |
| agent | role_prompt | 689/895 (77.0%) | 832/895 (93.0%) | 0.750 | 1 |
| other-actant | noun_prompt | 684/971 (70.4%) | 887/971 (91.3%) | 0.674 | 13 |
| other-actant | role_prompt | 505/971 (52.0%) | 783/971 (80.6%) | 0.533 | 7 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 1866, full_image_box 0.311, image_center_point 0.671, largest_role_box 0.554, other_actant_box 0.107, random_box 0.020
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): n_targets 895, full_image_box 0.352, image_center_point 0.769, largest_role_box 0.639, other_actant_box 0.107, random_box 0.026
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 971, full_image_box 0.273, image_center_point 0.582, largest_role_box 0.475, other_actant_box 0.107, random_box 0.018

Both actants hit with role prompts, by role pair (top 8): agent-item 97/202; agent-victim 37/66; agent-vehicle 13/54; agent-target 9/52; agent-tool 22/48; agent-destination 4/38; agent-student 11/37; agent-contact 21/31

### Agreement, all items, foil outcome = pair_correct (n=933)

- pointing = both actants, role prompt: pointing hit 366/933 (39.2%); kappa(foil, pointing) = 0.041; cells {'foil+point+': 351, 'foil+point-': 515, 'foil-point+': 15, 'foil-point-': 52}
- pointing = agent only, role prompt: pointing hit 689/933 (73.8%); kappa(foil, pointing) = 0.032; cells {'foil+point+': 644, 'foil+point-': 222, 'foil-point+': 45, 'foil-point-': 22}
- pointing = both actants, noun prompt: pointing hit 538/933 (57.7%); kappa(foil, pointing) = 0.057; cells {'foil+point+': 511, 'foil+point-': 355, 'foil-point+': 27, 'foil-point-': 40}
- kappa(foil, blind) = 0.034; cells {'foil+point+': 456, 'foil+point-': 410, 'foil-point+': 27, 'foil-point-': 40}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.80, blind=+0.47; intercept=+2.09; fit acc 0.928 vs majority 0.928
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.31, blind=+0.46; intercept=+2.12; fit acc 0.928 vs majority 0.928

### Agreement, detector-verified gold only, foil outcome = pair_correct (n=409)

- pointing = both actants, role prompt: pointing hit 231/409 (56.5%); kappa(foil, pointing) = 0.054; cells {'foil+point+': 224, 'foil+point-': 164, 'foil-point+': 7, 'foil-point-': 14}
- pointing = agent only, role prompt: pointing hit 349/409 (85.3%); kappa(foil, pointing) = 0.025; cells {'foil+point+': 332, 'foil+point-': 56, 'foil-point+': 17, 'foil-point-': 4}
- pointing = both actants, noun prompt: pointing hit 354/409 (86.6%); kappa(foil, pointing) = 0.062; cells {'foil+point+': 338, 'foil+point-': 50, 'foil-point+': 16, 'foil-point-': 5}
- kappa(foil, blind) = 0.054; cells {'foil+point+': 212, 'foil+point-': 176, 'foil-point+': 6, 'foil-point-': 15}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.86, blind=+0.93; intercept=+2.10; fit acc 0.949 vs majority 0.949
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.28, blind=+0.90; intercept=+2.29; fit acc 0.949 vs majority 0.949

### Agreement, all items, foil outcome = yes_correct (n=933)

- pointing = both actants, role prompt: pointing hit 366/933 (39.2%); kappa(foil, pointing) = 0.064; cells {'foil+point+': 308, 'foil+point-': 434, 'foil-point+': 58, 'foil-point-': 133}
- pointing = agent only, role prompt: pointing hit 689/933 (73.8%); kappa(foil, pointing) = 0.030; cells {'foil+point+': 553, 'foil+point-': 189, 'foil-point+': 136, 'foil-point-': 55}
- pointing = both actants, noun prompt: pointing hit 538/933 (57.7%); kappa(foil, pointing) = 0.095; cells {'foil+point+': 448, 'foil+point-': 294, 'foil-point+': 90, 'foil-point-': 101}
- kappa(foil, blind) = -0.005; cells {'foil+point+': 383, 'foil+point-': 359, 'foil-point+': 100, 'foil-point-': 91}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.47, blind=-0.03; intercept=+1.20; fit acc 0.795 vs majority 0.795
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.16, blind=-0.03; intercept=+1.26; fit acc 0.795 vs majority 0.795

### Agreement, detector-verified gold only, foil outcome = yes_correct (n=409)

- pointing = both actants, role prompt: pointing hit 231/409 (56.5%); kappa(foil, pointing) = 0.043; cells {'foil+point+': 191, 'foil+point-': 140, 'foil-point+': 40, 'foil-point-': 38}
- pointing = agent only, role prompt: pointing hit 349/409 (85.3%); kappa(foil, pointing) = -0.042; cells {'foil+point+': 280, 'foil+point-': 51, 'foil-point+': 69, 'foil-point-': 9}
- pointing = both actants, noun prompt: pointing hit 354/409 (86.6%); kappa(foil, pointing) = 0.045; cells {'foil+point+': 289, 'foil+point-': 42, 'foil-point+': 65, 'foil-point-': 13}
- kappa(foil, blind) = 0.026; cells {'foil+point+': 179, 'foil+point-': 152, 'foil-point+': 39, 'foil-point-': 39}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.25, blind=+0.17; intercept=+1.22; fit acc 0.809 vs majority 0.809
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=-0.29, blind=+0.15; intercept=+1.62; fit acc 0.809 vs majority 0.809

## action-replacement (630 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 566/630 (89.8%) |
| pairwise, order-debiased | 600/630 (95.2%) |
| blind pairwise (no image) | 315/630 (50.0%) |
| mean P(yes) caption / foil | 0.642 / 0.156 |

- agent pointing, role_prompt: IoU>=0.5 482/630 (76.5%), mean IoU 0.742
- agent pointing, noun_prompt: IoU>=0.5 474/630 (75.2%), mean IoU 0.725
- kappa(foil, agent pointing) = 0.012; cells {'foil+point+': 460, 'foil+point-': 140, 'foil-point+': 22, 'foil-point-': 8}
- kappa(foil, blind) = -0.019; cells {'foil+point+': 297, 'foil+point-': 303, 'foil-point+': 18, 'foil-point-': 12}
- logistic: foil_correct ~ pointing + blind: coef: pointing=+0.14, blind=-0.37; intercept=+3.09; fit acc 0.952 vs majority 0.952

## aro-relation (1228 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 1130/1228 (92.0%) |
| pairwise, order-debiased | 1183/1228 (96.3%) |
| blind pairwise (no image) | 693/1228 (56.4%) |
| mean P(yes) caption / foil | 0.856 / 0.370 |
| yes-rate (P(yes)>0.5) caption / foil | 0.879 / 0.351 |
| pairwise on the benchmark crop | 1186/1228 (96.6%) |

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| other-actant | noun_prompt | 2136/2456 (87.0%) | 2318/2456 (94.4%) | 0.804 | 2 |
| other-actant | role_prompt | 1409/2456 (57.4%) | 1894/2456 (77.1%) | 0.564 | 0 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 2456, full_image_box 0.281, image_center_point 0.634, largest_role_box 0.601, other_actant_box 0.202, random_box 0.021
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): 
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 2456, full_image_box 0.281, image_center_point 0.634, largest_role_box 0.601, other_actant_box 0.202, random_box 0.021

Both actants hit with role prompts, by role pair (top 8): object-subject 444/1228

### Agreement, all items, foil outcome = pair_correct (n=1228)

- pointing = both actants, role prompt: pointing hit 444/1228 (36.2%); kappa(foil, pointing) = 0.024; cells {'foil+point+': 437, 'foil+point-': 746, 'foil-point+': 7, 'foil-point-': 38}
- pointing = agent only, role prompt: pointing hit 0/1228 (0.0%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 0, 'foil+point-': 1183, 'foil-point+': 0, 'foil-point-': 45}
- pointing = both actants, noun prompt: pointing hit 942/1228 (76.7%); kappa(foil, pointing) = 0.016; cells {'foil+point+': 910, 'foil+point-': 273, 'foil-point+': 32, 'foil-point-': 13}
- kappa(foil, blind) = 0.027; cells {'foil+point+': 675, 'foil+point-': 508, 'foil-point+': 18, 'foil-point-': 27}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.96, blind=+0.59; intercept=+2.73; fit acc 0.963 vs majority 0.963
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+0.63; intercept=+2.96; fit acc 0.963 vs majority 0.963

### Agreement, all items, foil outcome = yes_correct (n=1228)

- pointing = both actants, role prompt: pointing hit 444/1228 (36.2%); kappa(foil, pointing) = 0.043; cells {'foil+point+': 425, 'foil+point-': 705, 'foil-point+': 19, 'foil-point-': 79}
- pointing = agent only, role prompt: pointing hit 0/1228 (0.0%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 0, 'foil+point-': 1130, 'foil-point+': 0, 'foil-point-': 98}
- pointing = both actants, noun prompt: pointing hit 942/1228 (76.7%); kappa(foil, pointing) = 0.031; cells {'foil+point+': 872, 'foil+point-': 258, 'foil-point+': 70, 'foil-point-': 28}
- kappa(foil, blind) = 0.034; cells {'foil+point+': 647, 'foil+point-': 483, 'foil-point+': 46, 'foil-point-': 52}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.85, blind=+0.36; intercept=+2.02; fit acc 0.920 vs majority 0.920
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+0.40; intercept=+2.24; fit acc 0.920 vs majority 0.920

## aro-spatial (300 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 251/300 (83.7%) |
| pairwise, order-debiased | 250/300 (83.3%) |
| blind pairwise (no image) | 136/300 (45.3%) |
| mean P(yes) caption / foil | 0.704 / 0.194 |
| yes-rate (P(yes)>0.5) caption / foil | 0.730 / 0.133 |
| pairwise on the benchmark crop | 267/300 (89.0%) |

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| other-actant | noun_prompt | 415/600 (69.2%) | 486/600 (81.0%) | 0.648 | 4 |
| other-actant | role_prompt | 107/600 (17.8%) | 198/600 (33.0%) | 0.216 | 0 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 600, full_image_box 0.035, image_center_point 0.393, largest_role_box 0.500, other_actant_box 0.000, random_box 0.014
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): 
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 600, full_image_box 0.035, image_center_point 0.393, largest_role_box 0.500, other_actant_box 0.000, random_box 0.014

Both actants hit with role prompts, by role pair (top 8): object-subject 4/300

### Agreement, all items, foil outcome = pair_correct (n=300)

- pointing = both actants, role prompt: pointing hit 4/300 (1.3%); kappa(foil, pointing) = -0.011; cells {'foil+point+': 2, 'foil+point-': 248, 'foil-point+': 2, 'foil-point-': 48}
- pointing = agent only, role prompt: pointing hit 0/300 (0.0%); kappa(foil, pointing) = 0.000; cells {'foil+point+': 0, 'foil+point-': 250, 'foil-point+': 0, 'foil-point-': 50}
- pointing = both actants, noun prompt: pointing hit 144/300 (48.0%); kappa(foil, pointing) = 0.091; cells {'foil+point+': 127, 'foil+point-': 123, 'foil-point+': 17, 'foil-point-': 33}
- kappa(foil, blind) = -0.054; cells {'foil+point+': 109, 'foil+point-': 141, 'foil-point+': 27, 'foil-point-': 23}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=-0.83, blind=-0.39; intercept=+1.81; fit acc 0.833 vs majority 0.833
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=-0.38; intercept=+1.80; fit acc 0.833 vs majority 0.833

### Agreement, all items, foil outcome = yes_correct (n=300)

- pointing = both actants, role prompt: pointing hit 4/300 (1.3%); kappa(foil, pointing) = -0.003; cells {'foil+point+': 3, 'foil+point-': 248, 'foil-point+': 1, 'foil-point-': 48}
- pointing = agent only, role prompt: pointing hit 0/300 (0.0%); kappa(foil, pointing) = 0.000; cells {'foil+point+': 0, 'foil+point-': 251, 'foil-point+': 0, 'foil-point-': 49}
- pointing = both actants, noun prompt: pointing hit 144/300 (48.0%); kappa(foil, pointing) = 0.098; cells {'foil+point+': 128, 'foil+point-': 123, 'foil-point+': 16, 'foil-point-': 33}
- kappa(foil, blind) = -0.035; cells {'foil+point+': 111, 'foil+point-': 140, 'foil-point+': 25, 'foil-point-': 24}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=-0.24, blind=-0.25; intercept=+1.76; fit acc 0.837 vs majority 0.837
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=-0.25; intercept=+1.75; fit acc 0.837 vs majority 0.837

## controls, actant-swap (933 items, 1866 role targets)

- text-only role resolution correct: 1685/1866 (90.3%) (agent 848/895 (94.7%), other 837/971 (86.2%))
- pointing hit, role prompt: unconditioned 1194/1866 (64.0%) | caption-conditioned 1248/1866 (66.9%) | noun prompt 1398/1866 (74.9%)
- caption-conditioned by target: agent 717/895 (80.1%), other 531/971 (54.7%)
- both participants by role: unconditioned 366/933 (39.2%) | conditioned 399/933 (42.8%)
- text resolved correctly but unconditioned pointing failed: 580/1685 (34.4%) of text-correct targets
- conflict pointing (foil caption in prompt), non-nested targets n=1666: image-consistent 1042/1666 (62.5%), text-following 263/1666 (15.8%), both 11/1666 (0.7%), neither 350/1666 (21.0%); nested pairs excluded: 200

## controls, aro-relation (1228 items, 2456 role targets)

- text-only role resolution correct: 2203/2456 (89.7%) (agent n/a, other 2203/2456 (89.7%))
- pointing hit, role prompt: unconditioned 1408/2456 (57.3%) | caption-conditioned 1784/2456 (72.6%) | noun prompt 2136/2456 (87.0%)
- caption-conditioned by target: agent n/a, other 1784/2456 (72.6%)
- both participants by role: unconditioned 440/1228 (35.8%) | conditioned 661/1228 (53.8%)
- text resolved correctly but unconditioned pointing failed: 911/2203 (41.4%) of text-correct targets
- conflict pointing (foil caption in prompt), non-nested targets n=1960: image-consistent 1068/1960 (54.5%), text-following 418/1960 (21.3%), both 57/1960 (2.9%), neither 417/1960 (21.3%); nested pairs excluded: 496

## blind likelihood baseline, actant-swap (933 items)

- caption more likely than foil (text only): 91.1% | clearly text-solvable (margin > 1.0 nat): 85.6% | balanced: 8.1% | foil preferred: 6.2%
- stratum solvable (n=799): foil pass 94.0%, both-by-role 38.2%, P(point | foil pass) 39.4%, cells {'foil+point+': 296, 'foil+point-': 455, 'foil-point+': 9, 'foil-point-': 39}
- stratum balanced (n=76): foil pass 85.5%, both-by-role 48.7%, P(point | foil pass) 50.8%, cells {'foil+point+': 33, 'foil+point-': 32, 'foil-point+': 4, 'foil-point-': 7}
- stratum foil_preferred (n=58): foil pass 86.2%, both-by-role 41.4%, P(point | foil pass) 44.0%, cells {'foil+point+': 22, 'foil+point-': 28, 'foil-point+': 2, 'foil-point-': 6}

## blind likelihood baseline, action-replacement (630 items)

- caption more likely than foil (text only): 67.5% | clearly text-solvable (margin > 1.0 nat): 60.2% | balanced: 12.7% | foil preferred: 27.1%

## blind likelihood baseline, aro-relation (1228 items)

- caption more likely than foil (text only): 94.7% | clearly text-solvable (margin > 1.0 nat): 91.2% | balanced: 5.9% | foil preferred: 2.9%
- stratum solvable (n=1121): foil pass 98.0%, both-by-role 37.6%, P(point | foil pass) 38.0%, cells {'foil+point+': 418, 'foil+point-': 681, 'foil-point+': 4, 'foil-point-': 18}
- stratum balanced (n=72): foil pass 80.6%, both-by-role 20.8%, P(point | foil pass) 24.1%, cells {'foil+point+': 14, 'foil+point-': 44, 'foil-point+': 1, 'foil-point-': 13}
- stratum foil_preferred (n=35): foil pass 74.3%, both-by-role 20.0%, P(point | foil pass) 19.2%, cells {'foil+point+': 5, 'foil+point-': 21, 'foil-point+': 2, 'foil-point-': 7}

## blind likelihood baseline, aro-spatial (300 items)

- caption more likely than foil (text only): 52.0% | clearly text-solvable (margin > 1.0 nat): 34.3% | balanced: 35.3% | foil preferred: 30.3%
- stratum solvable (n=103): foil pass 76.7%, both-by-role 1.9%, P(point | foil pass) 0.0%, cells {'foil+point+': 0, 'foil+point-': 79, 'foil-point+': 2, 'foil-point-': 22}
- stratum balanced (n=106): foil pass 86.8%, both-by-role 0.9%, P(point | foil pass) 1.1%, cells {'foil+point+': 1, 'foil+point-': 91, 'foil-point+': 0, 'foil-point-': 14}
- stratum foil_preferred (n=91): foil pass 86.8%, both-by-role 1.1%, P(point | foil pass) 1.3%, cells {'foil+point+': 1, 'foil+point-': 78, 'foil-point+': 0, 'foil-point-': 12}

