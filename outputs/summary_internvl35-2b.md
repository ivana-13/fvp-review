# Summary for internvl35-2b

Gold check available: 409 of 933 checked actant-swap items have both actant boxes confirmed by Grounding DINO.

## actant-swap (933 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 693/933 (74.3%) |
| pairwise, order-debiased | 834/933 (89.4%) |
| blind pairwise (no image) | 795/933 (85.2%) |
| mean P(yes) caption / foil | 0.590 / 0.340 |
| yes-rate (P(yes)>0.5) caption / foil | 0.588 / 0.297 |

Verb naming: strict 114/933 (12.2%), WordNet-synonym 137/933 (14.7%)

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| agent | noun_prompt | 682/895 (76.2%) | 829/895 (92.6%) | 0.681 | 0 |
| agent | role_prompt | 633/895 (70.7%) | 818/895 (91.4%) | 0.639 | 0 |
| other-actant | noun_prompt | 596/971 (61.4%) | 796/971 (82.0%) | 0.570 | 0 |
| other-actant | role_prompt | 390/971 (40.2%) | 702/971 (72.3%) | 0.424 | 0 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 1866, full_image_box 0.311, image_center_point 0.671, largest_role_box 0.554, other_actant_box 0.107, random_box 0.020
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): n_targets 895, full_image_box 0.352, image_center_point 0.769, largest_role_box 0.639, other_actant_box 0.107, random_box 0.026
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 971, full_image_box 0.273, image_center_point 0.582, largest_role_box 0.475, other_actant_box 0.107, random_box 0.018

Both actants hit with role prompts, by role pair (top 8): agent-item 68/202; agent-victim 27/66; agent-vehicle 11/54; agent-target 9/52; agent-tool 15/48; agent-destination 3/38; agent-student 13/37; agent-contact 16/31

### Agreement, all items, foil outcome = pair_correct (n=933)

- pointing = both actants, role prompt: pointing hit 278/933 (29.8%); kappa(foil, pointing) = 0.037; cells {'foil+point+': 260, 'foil+point-': 574, 'foil-point+': 18, 'foil-point-': 81}
- pointing = agent only, role prompt: pointing hit 633/933 (67.8%); kappa(foil, pointing) = 0.073; cells {'foil+point+': 578, 'foil+point-': 256, 'foil-point+': 55, 'foil-point-': 44}
- pointing = both actants, noun prompt: pointing hit 440/933 (47.2%); kappa(foil, pointing) = 0.015; cells {'foil+point+': 397, 'foil+point-': 437, 'foil-point+': 43, 'foil-point-': 56}
- kappa(foil, blind) = 0.138; cells {'foil+point+': 725, 'foil+point-': 109, 'foil-point+': 70, 'foil-point-': 29}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.65, blind=+0.95; intercept=+1.22; fit acc 0.894 vs majority 0.894
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.56, blind=+0.95; intercept=+1.02; fit acc 0.894 vs majority 0.894

### Agreement, detector-verified gold only, foil outcome = pair_correct (n=409)

- pointing = both actants, role prompt: pointing hit 167/409 (40.8%); kappa(foil, pointing) = 0.059; cells {'foil+point+': 158, 'foil+point-': 212, 'foil-point+': 9, 'foil-point-': 30}
- pointing = agent only, role prompt: pointing hit 319/409 (78.0%); kappa(foil, pointing) = 0.061; cells {'foil+point+': 292, 'foil+point-': 78, 'foil-point+': 27, 'foil-point-': 12}
- pointing = both actants, noun prompt: pointing hit 276/409 (67.5%); kappa(foil, pointing) = -0.023; cells {'foil+point+': 248, 'foil+point-': 122, 'foil-point+': 28, 'foil-point-': 11}
- kappa(foil, blind) = 0.081; cells {'foil+point+': 321, 'foil+point-': 49, 'foil-point+': 30, 'foil-point-': 9}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.78, blind=+0.56; intercept=+1.52; fit acc 0.905 vs majority 0.905
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.45, blind=+0.58; intercept=+1.44; fit acc 0.905 vs majority 0.905

### Agreement, all items, foil outcome = yes_correct (n=933)

- pointing = both actants, role prompt: pointing hit 278/933 (29.8%); kappa(foil, pointing) = 0.074; cells {'foil+point+': 227, 'foil+point-': 466, 'foil-point+': 51, 'foil-point-': 189}
- pointing = agent only, role prompt: pointing hit 633/933 (67.8%); kappa(foil, pointing) = -0.006; cells {'foil+point+': 469, 'foil+point-': 224, 'foil-point+': 164, 'foil-point-': 76}
- pointing = both actants, noun prompt: pointing hit 440/933 (47.2%); kappa(foil, pointing) = 0.063; cells {'foil+point+': 342, 'foil+point-': 351, 'foil-point+': 98, 'foil-point-': 142}
- kappa(foil, blind) = 0.003; cells {'foil+point+': 591, 'foil+point-': 102, 'foil-point+': 204, 'foil-point-': 36}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.57, blind=+0.00; intercept=+0.90; fit acc 0.743 vs majority 0.743
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=-0.03, blind=+0.02; intercept=+1.06; fit acc 0.743 vs majority 0.743

### Agreement, detector-verified gold only, foil outcome = yes_correct (n=409)

- pointing = both actants, role prompt: pointing hit 167/409 (40.8%); kappa(foil, pointing) = 0.092; cells {'foil+point+': 139, 'foil+point-': 176, 'foil-point+': 28, 'foil-point-': 66}
- pointing = agent only, role prompt: pointing hit 319/409 (78.0%); kappa(foil, pointing) = -0.038; cells {'foil+point+': 243, 'foil+point-': 72, 'foil-point+': 76, 'foil-point-': 18}
- pointing = both actants, noun prompt: pointing hit 276/409 (67.5%); kappa(foil, pointing) = 0.017; cells {'foil+point+': 214, 'foil+point-': 101, 'foil-point+': 62, 'foil-point-': 32}
- kappa(foil, blind) = -0.085; cells {'foil+point+': 265, 'foil+point-': 50, 'foil-point+': 86, 'foil-point-': 8}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.60, blind=-0.64; intercept=+1.55; fit acc 0.770 vs majority 0.770
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=-0.21, blind=-0.61; intercept=+1.91; fit acc 0.770 vs majority 0.770

## action-replacement (630 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 550/630 (87.3%) |
| pairwise, order-debiased | 586/630 (93.0%) |
| blind pairwise (no image) | 395/630 (62.7%) |
| mean P(yes) caption / foil | 0.597 / 0.177 |

- agent pointing, role_prompt: IoU>=0.5 452/630 (71.7%), mean IoU 0.646
- agent pointing, noun_prompt: IoU>=0.5 456/630 (72.4%), mean IoU 0.646
- kappa(foil, agent pointing) = 0.046; cells {'foil+point+': 425, 'foil+point-': 161, 'foil-point+': 27, 'foil-point-': 17}
- kappa(foil, blind) = 0.029; cells {'foil+point+': 371, 'foil+point-': 215, 'foil-point+': 24, 'foil-point-': 20}
- logistic: foil_correct ~ pointing + blind: coef: pointing=+0.49, blind=+0.37; intercept=+2.04; fit acc 0.930 vs majority 0.930

## aro-relation (1228 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 1111/1228 (90.5%) |
| pairwise, order-debiased | 1183/1228 (96.3%) |
| blind pairwise (no image) | 1037/1228 (84.4%) |
| mean P(yes) caption / foil | 0.797 / 0.326 |
| yes-rate (P(yes)>0.5) caption / foil | 0.811 / 0.279 |
| pairwise on the benchmark crop | 1181/1228 (96.2%) |

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| other-actant | noun_prompt | 1899/2456 (77.3%) | 2186/2456 (89.0%) | 0.722 | 0 |
| other-actant | role_prompt | 1293/2456 (52.6%) | 1813/2456 (73.8%) | 0.521 | 0 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 2456, full_image_box 0.281, image_center_point 0.634, largest_role_box 0.601, other_actant_box 0.202, random_box 0.021
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): 
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 2456, full_image_box 0.281, image_center_point 0.634, largest_role_box 0.601, other_actant_box 0.202, random_box 0.021

Both actants hit with role prompts, by role pair (top 8): object-subject 398/1228

### Agreement, all items, foil outcome = pair_correct (n=1228)

- pointing = both actants, role prompt: pointing hit 398/1228 (32.4%); kappa(foil, pointing) = 0.016; cells {'foil+point+': 390, 'foil+point-': 793, 'foil-point+': 8, 'foil-point-': 37}
- pointing = agent only, role prompt: pointing hit 0/1228 (0.0%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 0, 'foil+point-': 1183, 'foil-point+': 0, 'foil-point-': 45}
- pointing = both actants, noun prompt: pointing hit 742/1228 (60.4%); kappa(foil, pointing) = 0.001; cells {'foil+point+': 715, 'foil+point-': 468, 'foil-point+': 27, 'foil-point-': 18}
- kappa(foil, blind) = 0.117; cells {'foil+point+': 1012, 'foil+point-': 171, 'foil-point+': 25, 'foil-point-': 20}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.55, blind=+1.35; intercept=+2.14; fit acc 0.963 vs majority 0.963
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+1.42; intercept=+2.23; fit acc 0.963 vs majority 0.963

### Agreement, all items, foil outcome = yes_correct (n=1228)

- pointing = both actants, role prompt: pointing hit 398/1228 (32.4%); kappa(foil, pointing) = 0.023; cells {'foil+point+': 369, 'foil+point-': 742, 'foil-point+': 29, 'foil-point-': 88}
- pointing = agent only, role prompt: pointing hit 0/1228 (0.0%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 0, 'foil+point-': 1111, 'foil-point+': 0, 'foil-point-': 117}
- pointing = both actants, noun prompt: pointing hit 742/1228 (60.4%); kappa(foil, pointing) = 0.022; cells {'foil+point+': 677, 'foil+point-': 434, 'foil-point+': 65, 'foil-point-': 52}
- kappa(foil, blind) = 0.021; cells {'foil+point+': 941, 'foil+point-': 170, 'foil-point+': 96, 'foil-point-': 21}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.38, blind=+0.12; intercept=+2.04; fit acc 0.905 vs majority 0.905
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+0.18; intercept=+2.10; fit acc 0.905 vs majority 0.905

## aro-spatial (300 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 241/300 (80.3%) |
| pairwise, order-debiased | 240/300 (80.0%) |
| blind pairwise (no image) | 139/300 (46.3%) |
| mean P(yes) caption / foil | 0.499 / 0.094 |
| yes-rate (P(yes)>0.5) caption / foil | 0.480 / 0.030 |
| pairwise on the benchmark crop | 265/300 (88.3%) |

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| other-actant | noun_prompt | 328/600 (54.7%) | 423/600 (70.5%) | 0.537 | 0 |
| other-actant | role_prompt | 88/600 (14.7%) | 174/600 (29.0%) | 0.183 | 0 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 600, full_image_box 0.035, image_center_point 0.393, largest_role_box 0.500, other_actant_box 0.000, random_box 0.014
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): 
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 600, full_image_box 0.035, image_center_point 0.393, largest_role_box 0.500, other_actant_box 0.000, random_box 0.014

Both actants hit with role prompts, by role pair (top 8): object-subject 0/300

### Agreement, all items, foil outcome = pair_correct (n=300)

- pointing = both actants, role prompt: pointing hit 0/300 (0.0%); kappa(foil, pointing) = 0.000; cells {'foil+point+': 0, 'foil+point-': 240, 'foil-point+': 0, 'foil-point-': 60}
- pointing = agent only, role prompt: pointing hit 0/300 (0.0%); kappa(foil, pointing) = 0.000; cells {'foil+point+': 0, 'foil+point-': 240, 'foil-point+': 0, 'foil-point-': 60}
- pointing = both actants, noun prompt: pointing hit 98/300 (32.7%); kappa(foil, pointing) = 0.172; cells {'foil+point+': 94, 'foil+point-': 146, 'foil-point+': 4, 'foil-point-': 56}
- kappa(foil, blind) = -0.041; cells {'foil+point+': 108, 'foil+point-': 132, 'foil-point+': 31, 'foil-point-': 29}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.00, blind=-0.25; intercept=+1.50; fit acc 0.800 vs majority 0.800
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=-0.25; intercept=+1.50; fit acc 0.800 vs majority 0.800

### Agreement, all items, foil outcome = yes_correct (n=300)

- pointing = both actants, role prompt: pointing hit 0/300 (0.0%); kappa(foil, pointing) = 0.000; cells {'foil+point+': 0, 'foil+point-': 241, 'foil-point+': 0, 'foil-point-': 59}
- pointing = agent only, role prompt: pointing hit 0/300 (0.0%); kappa(foil, pointing) = 0.000; cells {'foil+point+': 0, 'foil+point-': 241, 'foil-point+': 0, 'foil-point-': 59}
- pointing = both actants, noun prompt: pointing hit 98/300 (32.7%); kappa(foil, pointing) = 0.168; cells {'foil+point+': 94, 'foil+point-': 147, 'foil-point+': 4, 'foil-point-': 55}
- kappa(foil, blind) = -0.060; cells {'foil+point+': 107, 'foil+point-': 134, 'foil-point+': 32, 'foil-point-': 27}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.00, blind=-0.36; intercept=+1.59; fit acc 0.803 vs majority 0.803
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=-0.36; intercept=+1.59; fit acc 0.803 vs majority 0.803

## controls, actant-swap (933 items, 1866 role targets)

- text-only role resolution correct: 1597/1866 (85.6%) (agent 846/895 (94.5%), other 751/971 (77.3%))
- pointing hit, role prompt: unconditioned 1023/1866 (54.8%) | caption-conditioned 1099/1866 (58.9%) | noun prompt 1278/1866 (68.5%)
- caption-conditioned by target: agent 647/895 (72.3%), other 452/971 (46.5%)
- both participants by role: unconditioned 278/933 (29.8%) | conditioned 327/933 (35.0%)
- text resolved correctly but unconditioned pointing failed: 671/1597 (42.0%) of text-correct targets
- conflict pointing (foil caption in prompt), non-nested targets n=1666: image-consistent 889/1666 (53.4%), text-following 197/1666 (11.8%), both 12/1666 (0.7%), neither 568/1666 (34.1%); nested pairs excluded: 200

## controls, aro-relation (1228 items, 2456 role targets)

- text-only role resolution correct: 1851/2456 (75.4%) (agent n/a, other 1851/2456 (75.4%))
- pointing hit, role prompt: unconditioned 1290/2456 (52.5%) | caption-conditioned 1586/2456 (64.6%) | noun prompt 1899/2456 (77.3%)
- caption-conditioned by target: agent n/a, other 1586/2456 (64.6%)
- both participants by role: unconditioned 396/1228 (32.2%) | conditioned 538/1228 (43.8%)
- text resolved correctly but unconditioned pointing failed: 801/1851 (43.3%) of text-correct targets
- conflict pointing (foil caption in prompt), non-nested targets n=1960: image-consistent 1073/1960 (54.7%), text-following 328/1960 (16.7%), both 46/1960 (2.3%), neither 513/1960 (26.2%); nested pairs excluded: 496

## blind likelihood baseline, actant-swap (933 items)

- caption more likely than foil (text only): 90.9% | clearly text-solvable (margin > 1.0 nat): 86.5% | balanced: 7.4% | foil preferred: 6.1%
- stratum solvable (n=807): foil pass 90.7%, both-by-role 28.9%, P(point | foil pass) 30.1%, cells {'foil+point+': 220, 'foil+point-': 512, 'foil-point+': 13, 'foil-point-': 62}
- stratum balanced (n=69): foil pass 81.2%, both-by-role 37.7%, P(point | foil pass) 39.3%, cells {'foil+point+': 22, 'foil+point-': 34, 'foil-point+': 4, 'foil-point-': 9}
- stratum foil_preferred (n=57): foil pass 80.7%, both-by-role 33.3%, P(point | foil pass) 39.1%, cells {'foil+point+': 18, 'foil+point-': 28, 'foil-point+': 1, 'foil-point-': 10}

## blind likelihood baseline, action-replacement (630 items)

- caption more likely than foil (text only): 66.8% | clearly text-solvable (margin > 1.0 nat): 60.5% | balanced: 14.1% | foil preferred: 25.4%

## blind likelihood baseline, aro-relation (1228 items)

- caption more likely than foil (text only): 95.0% | clearly text-solvable (margin > 1.0 nat): 92.1% | balanced: 5.0% | foil preferred: 2.9%
- stratum solvable (n=1130): foil pass 98.1%, both-by-role 33.9%, P(point | foil pass) 34.2%, cells {'foil+point+': 379, 'foil+point-': 729, 'foil-point+': 4, 'foil-point-': 18}
- stratum balanced (n=63): foil pass 76.2%, both-by-role 17.5%, P(point | foil pass) 18.8%, cells {'foil+point+': 9, 'foil+point-': 39, 'foil-point+': 2, 'foil-point-': 13}
- stratum foil_preferred (n=35): foil pass 77.1%, both-by-role 11.4%, P(point | foil pass) 7.4%, cells {'foil+point+': 2, 'foil+point-': 25, 'foil-point+': 2, 'foil-point-': 6}

## blind likelihood baseline, aro-spatial (300 items)

- caption more likely than foil (text only): 52.7% | clearly text-solvable (margin > 1.0 nat): 33.3% | balanced: 35.7% | foil preferred: 31.0%
- stratum solvable (n=100): foil pass 73.0%, both-by-role 0.0%, P(point | foil pass) 0.0%, cells {'foil+point+': 0, 'foil+point-': 73, 'foil-point+': 0, 'foil-point-': 27}
- stratum balanced (n=107): foil pass 83.2%, both-by-role 0.0%, P(point | foil pass) 0.0%, cells {'foil+point+': 0, 'foil+point-': 89, 'foil-point+': 0, 'foil-point-': 18}
- stratum foil_preferred (n=93): foil pass 83.9%, both-by-role 0.0%, P(point | foil pass) 0.0%, cells {'foil+point+': 0, 'foil+point-': 78, 'foil-point+': 0, 'foil-point-': 15}

