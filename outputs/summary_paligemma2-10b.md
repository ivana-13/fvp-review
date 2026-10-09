# Summary for paligemma2-10b

Gold check available: 409 of 933 checked actant-swap items have both actant boxes confirmed by Grounding DINO.

## actant-swap (933 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 791/933 (84.8%) |
| pairwise, order-debiased | 859/933 (92.1%) |
| blind pairwise (no image) | 638/933 (68.4%) |
| mean P(yes) caption / foil | 0.509 / 0.359 |
| yes-rate (P(yes)>0.5) caption / foil | 0.555 / 0.169 |

Verb naming: strict 181/933 (19.4%), WordNet-synonym 230/933 (24.7%)

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| agent | noun_prompt | 686/895 (76.6%) | 755/895 (84.4%) | 0.729 | 110 |
| agent | role_prompt | 675/895 (75.4%) | 814/895 (90.9%) | 0.739 | 0 |
| other-actant | noun_prompt | 568/971 (58.5%) | 661/971 (68.1%) | 0.548 | 255 |
| other-actant | role_prompt | 564/971 (58.1%) | 761/971 (78.4%) | 0.581 | 5 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 1866, full_image_box 0.311, image_center_point 0.671, largest_role_box 0.554, other_actant_box 0.107, random_box 0.020
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): n_targets 895, full_image_box 0.352, image_center_point 0.769, largest_role_box 0.639, other_actant_box 0.107, random_box 0.026
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 971, full_image_box 0.273, image_center_point 0.582, largest_role_box 0.475, other_actant_box 0.107, random_box 0.018

Both actants hit with role prompts, by role pair (top 8): agent-item 94/202; agent-victim 37/66; agent-vehicle 19/54; agent-target 15/52; agent-tool 23/48; agent-destination 11/38; agent-student 15/37; agent-contact 19/31

### Agreement, all items, foil outcome = pair_correct (n=933)

- pointing = both actants, role prompt: pointing hit 406/933 (43.5%); kappa(foil, pointing) = -0.003; cells {'foil+point+': 373, 'foil+point-': 486, 'foil-point+': 33, 'foil-point-': 41}
- pointing = agent only, role prompt: pointing hit 675/933 (72.3%); kappa(foil, pointing) = 0.045; cells {'foil+point+': 628, 'foil+point-': 231, 'foil-point+': 47, 'foil-point-': 27}
- pointing = both actants, noun prompt: pointing hit 427/933 (45.8%); kappa(foil, pointing) = 0.007; cells {'foil+point+': 395, 'foil+point-': 464, 'foil-point+': 32, 'foil-point-': 42}
- kappa(foil, blind) = 0.171; cells {'foil+point+': 615, 'foil+point-': 244, 'foil-point+': 23, 'foil-point-': 51}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=-0.02, blind=+1.62; intercept=+1.61; fit acc 0.921 vs majority 0.921
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.43, blind=+1.62; intercept=+1.31; fit acc 0.921 vs majority 0.921

### Agreement, detector-verified gold only, foil outcome = pair_correct (n=409)

- pointing = both actants, role prompt: pointing hit 235/409 (57.5%); kappa(foil, pointing) = -0.063; cells {'foil+point+': 211, 'foil+point-': 166, 'foil-point+': 24, 'foil-point-': 8}
- pointing = agent only, role prompt: pointing hit 337/409 (82.4%); kappa(foil, pointing) = 0.008; cells {'foil+point+': 311, 'foil+point-': 66, 'foil-point+': 26, 'foil-point-': 6}
- pointing = both actants, noun prompt: pointing hit 271/409 (66.3%); kappa(foil, pointing) = -0.011; cells {'foil+point+': 249, 'foil+point-': 128, 'foil-point+': 22, 'foil-point-': 10}
- kappa(foil, blind) = 0.169; cells {'foil+point+': 270, 'foil+point-': 107, 'foil-point+': 10, 'foil-point-': 22}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=-0.69, blind=+1.47; intercept=+2.12; fit acc 0.922 vs majority 0.922
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.06, blind=+1.49; intercept=+1.61; fit acc 0.922 vs majority 0.922

### Agreement, all items, foil outcome = yes_correct (n=933)

- pointing = both actants, role prompt: pointing hit 406/933 (43.5%); kappa(foil, pointing) = 0.023; cells {'foil+point+': 350, 'foil+point-': 441, 'foil-point+': 56, 'foil-point-': 86}
- pointing = agent only, role prompt: pointing hit 675/933 (72.3%); kappa(foil, pointing) = 0.061; cells {'foil+point+': 582, 'foil+point-': 209, 'foil-point+': 93, 'foil-point-': 49}
- pointing = both actants, noun prompt: pointing hit 427/933 (45.8%); kappa(foil, pointing) = 0.004; cells {'foil+point+': 363, 'foil+point-': 428, 'foil-point+': 64, 'foil-point-': 78}
- kappa(foil, blind) = 0.173; cells {'foil+point+': 571, 'foil+point-': 220, 'foil-point+': 67, 'foil-point-': 75}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.21, blind=+1.03; intercept=+1.01; fit acc 0.848 vs majority 0.848
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.37, blind=+1.03; intercept=+0.84; fit acc 0.848 vs majority 0.848

### Agreement, detector-verified gold only, foil outcome = yes_correct (n=409)

- pointing = both actants, role prompt: pointing hit 235/409 (57.5%); kappa(foil, pointing) = -0.007; cells {'foil+point+': 201, 'foil+point-': 150, 'foil-point+': 34, 'foil-point-': 24}
- pointing = agent only, role prompt: pointing hit 337/409 (82.4%); kappa(foil, pointing) = 0.051; cells {'foil+point+': 292, 'foil+point-': 59, 'foil-point+': 45, 'foil-point-': 13}
- pointing = both actants, noun prompt: pointing hit 271/409 (66.3%); kappa(foil, pointing) = -0.058; cells {'foil+point+': 228, 'foil+point-': 123, 'foil-point+': 43, 'foil-point-': 15}
- kappa(foil, blind) = 0.156; cells {'foil+point+': 252, 'foil+point-': 99, 'foil-point+': 28, 'foil-point-': 30}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=-0.01, blind=+0.93; intercept=+1.24; fit acc 0.858 vs majority 0.858
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.32, blind=+0.93; intercept=+0.97; fit acc 0.858 vs majority 0.858

## action-replacement (630 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 540/630 (85.7%) |
| pairwise, order-debiased | 581/630 (92.2%) |
| blind pairwise (no image) | 402/630 (63.8%) |
| mean P(yes) caption / foil | 0.514 / 0.302 |

- agent pointing, role_prompt: IoU>=0.5 491/630 (77.9%), mean IoU 0.756
- agent pointing, noun_prompt: IoU>=0.5 471/630 (74.8%), mean IoU 0.707
- kappa(foil, agent pointing) = -0.034; cells {'foil+point+': 450, 'foil+point-': 131, 'foil-point+': 41, 'foil-point-': 8}
- kappa(foil, blind) = 0.019; cells {'foil+point+': 373, 'foil+point-': 208, 'foil-point+': 29, 'foil-point-': 20}
- logistic: foil_correct ~ pointing + blind: coef: pointing=-0.35, blind=+0.20; intercept=+2.63; fit acc 0.922 vs majority 0.922

## aro-relation (1228 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 1169/1228 (95.2%) |
| pairwise, order-debiased | 1183/1228 (96.3%) |
| blind pairwise (no image) | 370/1228 (30.1%) |
| mean P(yes) caption / foil | 0.604 / 0.270 |
| yes-rate (P(yes)>0.5) caption / foil | 0.830 / 0.107 |
| pairwise on the benchmark crop | 1182/1228 (96.3%) |

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| other-actant | noun_prompt | 1611/2456 (65.6%) | 1709/2456 (69.6%) | 0.618 | 650 |
| other-actant | role_prompt | 1526/2456 (62.1%) | 1919/2456 (78.1%) | 0.616 | 49 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 2456, full_image_box 0.281, image_center_point 0.634, largest_role_box 0.601, other_actant_box 0.202, random_box 0.021
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): 
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 2456, full_image_box 0.281, image_center_point 0.634, largest_role_box 0.601, other_actant_box 0.202, random_box 0.021

Both actants hit with role prompts, by role pair (top 8): object-subject 496/1228

### Agreement, all items, foil outcome = pair_correct (n=1228)

- pointing = both actants, role prompt: pointing hit 496/1228 (40.4%); kappa(foil, pointing) = 0.036; cells {'foil+point+': 491, 'foil+point-': 692, 'foil-point+': 5, 'foil-point-': 40}
- pointing = agent only, role prompt: pointing hit 0/1228 (0.0%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 0, 'foil+point-': 1183, 'foil-point+': 0, 'foil-point-': 45}
- pointing = both actants, noun prompt: pointing hit 562/1228 (45.8%); kappa(foil, pointing) = 0.014; cells {'foil+point+': 546, 'foil+point-': 637, 'foil-point+': 16, 'foil-point-': 29}
- kappa(foil, blind) = 0.004; cells {'foil+point+': 358, 'foil+point-': 825, 'foil-point+': 12, 'foil-point-': 33}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+1.44, blind=+0.23; intercept=+2.82; fit acc 0.963 vs majority 0.963
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+0.16; intercept=+3.23; fit acc 0.963 vs majority 0.963

### Agreement, all items, foil outcome = yes_correct (n=1228)

- pointing = both actants, role prompt: pointing hit 496/1228 (40.4%); kappa(foil, pointing) = 0.044; cells {'foil+point+': 488, 'foil+point-': 681, 'foil-point+': 8, 'foil-point-': 51}
- pointing = agent only, role prompt: pointing hit 0/1228 (0.0%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 0, 'foil+point-': 1169, 'foil-point+': 0, 'foil-point-': 59}
- pointing = both actants, noun prompt: pointing hit 562/1228 (45.8%); kappa(foil, pointing) = 0.021; cells {'foil+point+': 542, 'foil+point-': 627, 'foil-point+': 20, 'foil-point-': 39}
- kappa(foil, blind) = -0.005; cells {'foil+point+': 350, 'foil+point-': 819, 'foil-point+': 20, 'foil-point-': 39}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+1.32, blind=-0.09; intercept=+2.65; fit acc 0.952 vs majority 0.952
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=-0.17; intercept=+3.04; fit acc 0.952 vs majority 0.952

## aro-spatial (300 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 251/300 (83.7%) |
| pairwise, order-debiased | 227/300 (75.7%) |
| blind pairwise (no image) | 160/300 (53.3%) |
| mean P(yes) caption / foil | 0.452 / 0.213 |
| yes-rate (P(yes)>0.5) caption / foil | 0.347 / 0.017 |
| pairwise on the benchmark crop | 258/300 (86.0%) |

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| other-actant | noun_prompt | 288/600 (48.0%) | 315/600 (52.5%) | 0.454 | 220 |
| other-actant | role_prompt | 134/600 (22.3%) | 273/600 (45.5%) | 0.304 | 43 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 600, full_image_box 0.035, image_center_point 0.393, largest_role_box 0.500, other_actant_box 0.000, random_box 0.014
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): 
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 600, full_image_box 0.035, image_center_point 0.393, largest_role_box 0.500, other_actant_box 0.000, random_box 0.014

Both actants hit with role prompts, by role pair (top 8): object-subject 10/300

### Agreement, all items, foil outcome = pair_correct (n=300)

- pointing = both actants, role prompt: pointing hit 10/300 (3.3%); kappa(foil, pointing) = 0.013; cells {'foil+point+': 9, 'foil+point-': 218, 'foil-point+': 1, 'foil-point-': 72}
- pointing = agent only, role prompt: pointing hit 0/300 (0.0%); kappa(foil, pointing) = 0.000; cells {'foil+point+': 0, 'foil+point-': 227, 'foil-point+': 0, 'foil-point-': 73}
- pointing = both actants, noun prompt: pointing hit 71/300 (23.7%); kappa(foil, pointing) = 0.087; cells {'foil+point+': 62, 'foil+point-': 165, 'foil-point+': 9, 'foil-point-': 64}
- kappa(foil, blind) = 0.123; cells {'foil+point+': 130, 'foil+point-': 97, 'foil-point+': 30, 'foil-point-': 43}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.62, blind=+0.62; intercept=+0.81; fit acc 0.757 vs majority 0.757
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+0.61; intercept=+0.83; fit acc 0.757 vs majority 0.757

### Agreement, all items, foil outcome = yes_correct (n=300)

- pointing = both actants, role prompt: pointing hit 10/300 (3.3%); kappa(foil, pointing) = 0.013; cells {'foil+point+': 10, 'foil+point-': 241, 'foil-point+': 0, 'foil-point-': 49}
- pointing = agent only, role prompt: pointing hit 0/300 (0.0%); kappa(foil, pointing) = 0.000; cells {'foil+point+': 0, 'foil+point-': 251, 'foil-point+': 0, 'foil-point-': 49}
- pointing = both actants, noun prompt: pointing hit 71/300 (23.7%); kappa(foil, pointing) = 0.065; cells {'foil+point+': 66, 'foil+point-': 185, 'foil-point+': 5, 'foil-point-': 44}
- kappa(foil, blind) = 0.072; cells {'foil+point+': 139, 'foil+point-': 112, 'foil-point+': 21, 'foil-point-': 28}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.84, blind=+0.47; intercept=+1.38; fit acc 0.837 vs majority 0.837
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+0.46; intercept=+1.41; fit acc 0.837 vs majority 0.837

## controls, actant-swap (933 items, 1866 role targets)

- text-only role resolution correct: 1179/1866 (63.2%) (agent 673/895 (75.2%), other 506/971 (52.1%))
- pointing hit, role prompt: unconditioned 1239/1866 (66.4%) | caption-conditioned 857/1866 (45.9%) | noun prompt 1254/1866 (67.2%)
- caption-conditioned by target: agent 432/895 (48.3%), other 425/971 (43.8%)
- both participants by role: unconditioned 406/933 (43.5%) | conditioned 213/933 (22.8%)
- text resolved correctly but unconditioned pointing failed: 344/1179 (29.2%) of text-correct targets
- conflict pointing (foil caption in prompt), non-nested targets n=1666: image-consistent 655/1666 (39.3%), text-following 191/1666 (11.5%), both 87/1666 (5.2%), neither 733/1666 (44.0%); nested pairs excluded: 200

## controls, aro-relation (1228 items, 2456 role targets)

- text-only role resolution correct: 1876/2456 (76.4%) (agent n/a, other 1876/2456 (76.4%))
- pointing hit, role prompt: unconditioned 1527/2456 (62.2%) | caption-conditioned 1444/2456 (58.8%) | noun prompt 1611/2456 (65.6%)
- caption-conditioned by target: agent n/a, other 1444/2456 (58.8%)
- both participants by role: unconditioned 496/1228 (40.4%) | conditioned 409/1228 (33.3%)
- text resolved correctly but unconditioned pointing failed: 661/1876 (35.2%) of text-correct targets
- conflict pointing (foil caption in prompt), non-nested targets n=1960: image-consistent 973/1960 (49.6%), text-following 364/1960 (18.6%), both 96/1960 (4.9%), neither 527/1960 (26.9%); nested pairs excluded: 496

## blind likelihood baseline, actant-swap (933 items)

- caption more likely than foil (text only): 57.0% | clearly text-solvable (margin > 1.0 nat): 50.7% | balanced: 12.9% | foil preferred: 36.4%
- stratum solvable (n=473): foil pass 90.9%, both-by-role 44.0%, P(point | foil pass) 43.5%, cells {'foil+point+': 187, 'foil+point-': 243, 'foil-point+': 21, 'foil-point-': 22}
- stratum balanced (n=120): foil pass 90.8%, both-by-role 40.8%, P(point | foil pass) 41.3%, cells {'foil+point+': 45, 'foil+point-': 64, 'foil-point+': 4, 'foil-point-': 7}
- stratum foil_preferred (n=340): foil pass 94.1%, both-by-role 43.8%, P(point | foil pass) 44.1%, cells {'foil+point+': 141, 'foil+point-': 179, 'foil-point+': 8, 'foil-point-': 12}

## blind likelihood baseline, action-replacement (630 items)

- caption more likely than foil (text only): 59.2% | clearly text-solvable (margin > 1.0 nat): 50.6% | balanced: 15.1% | foil preferred: 34.3%

## blind likelihood baseline, aro-relation (1228 items)

- caption more likely than foil (text only): 79.2% | clearly text-solvable (margin > 1.0 nat): 73.6% | balanced: 10.4% | foil preferred: 16.0%
- stratum solvable (n=907): foil pass 97.1%, both-by-role 41.5%, P(point | foil pass) 42.3%, cells {'foil+point+': 373, 'foil+point-': 508, 'foil-point+': 3, 'foil-point-': 23}
- stratum balanced (n=126): foil pass 94.4%, both-by-role 41.3%, P(point | foil pass) 42.9%, cells {'foil+point+': 51, 'foil+point-': 68, 'foil-point+': 1, 'foil-point-': 6}
- stratum foil_preferred (n=195): foil pass 93.8%, both-by-role 34.9%, P(point | foil pass) 36.6%, cells {'foil+point+': 67, 'foil+point-': 116, 'foil-point+': 1, 'foil-point-': 11}

## blind likelihood baseline, aro-spatial (300 items)

- caption more likely than foil (text only): 56.0% | clearly text-solvable (margin > 1.0 nat): 47.3% | balanced: 16.0% | foil preferred: 36.7%
- stratum solvable (n=142): foil pass 76.8%, both-by-role 2.1%, P(point | foil pass) 1.8%, cells {'foil+point+': 2, 'foil+point-': 107, 'foil-point+': 1, 'foil-point-': 32}
- stratum balanced (n=48): foil pass 83.3%, both-by-role 2.1%, P(point | foil pass) 2.5%, cells {'foil+point+': 1, 'foil+point-': 39, 'foil-point+': 0, 'foil-point-': 8}
- stratum foil_preferred (n=110): foil pass 70.9%, both-by-role 5.5%, P(point | foil pass) 7.7%, cells {'foil+point+': 6, 'foil+point-': 72, 'foil-point+': 0, 'foil-point-': 32}

