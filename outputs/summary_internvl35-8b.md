# Summary for internvl35-8b

Gold check available: 409 of 933 checked actant-swap items have both actant boxes confirmed by Grounding DINO.

## actant-swap (933 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 863/933 (92.5%) |
| pairwise, order-debiased | 892/933 (95.6%) |
| blind pairwise (no image) | 677/933 (72.6%) |
| mean P(yes) caption / foil | 0.633 / 0.103 |
| yes-rate (P(yes)>0.5) caption / foil | 0.643 / 0.080 |

Verb naming: strict 161/933 (17.3%), WordNet-synonym 189/933 (20.3%)

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| agent | noun_prompt | 724/895 (80.9%) | 838/895 (93.6%) | 0.760 | 0 |
| agent | role_prompt | 664/895 (74.2%) | 818/895 (91.4%) | 0.709 | 0 |
| other-actant | noun_prompt | 632/971 (65.1%) | 803/971 (82.7%) | 0.621 | 0 |
| other-actant | role_prompt | 531/971 (54.7%) | 804/971 (82.8%) | 0.545 | 1 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 1866, full_image_box 0.311, image_center_point 0.671, largest_role_box 0.554, other_actant_box 0.107, random_box 0.020
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): n_targets 895, full_image_box 0.352, image_center_point 0.769, largest_role_box 0.639, other_actant_box 0.107, random_box 0.026
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 971, full_image_box 0.273, image_center_point 0.582, largest_role_box 0.475, other_actant_box 0.107, random_box 0.018

Both actants hit with role prompts, by role pair (top 8): agent-item 90/202; agent-victim 33/66; agent-vehicle 12/54; agent-target 16/52; agent-tool 19/48; agent-destination 5/38; agent-student 15/37; agent-contact 22/31

### Agreement, all items, foil outcome = pair_correct (n=933)

- pointing = both actants, role prompt: pointing hit 381/933 (40.8%); kappa(foil, pointing) = 0.025; cells {'foil+point+': 371, 'foil+point-': 521, 'foil-point+': 10, 'foil-point-': 31}
- pointing = agent only, role prompt: pointing hit 664/933 (71.2%); kappa(foil, pointing) = 0.057; cells {'foil+point+': 643, 'foil+point-': 249, 'foil-point+': 21, 'foil-point-': 20}
- pointing = both actants, noun prompt: pointing hit 486/933 (52.1%); kappa(foil, pointing) = 0.028; cells {'foil+point+': 471, 'foil+point-': 421, 'foil-point+': 15, 'foil-point-': 26}
- kappa(foil, blind) = 0.078; cells {'foil+point+': 658, 'foil+point-': 234, 'foil-point+': 19, 'foil-point-': 22}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.72, blind=+1.08; intercept=+2.17; fit acc 0.956 vs majority 0.956
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.92, blind=+1.16; intercept=+1.79; fit acc 0.956 vs majority 0.956

### Agreement, detector-verified gold only, foil outcome = pair_correct (n=409)

- pointing = both actants, role prompt: pointing hit 228/409 (55.7%); kappa(foil, pointing) = 0.036; cells {'foil+point+': 224, 'foil+point-': 172, 'foil-point+': 4, 'foil-point-': 9}
- pointing = agent only, role prompt: pointing hit 327/409 (80.0%); kappa(foil, pointing) = 0.120; cells {'foil+point+': 322, 'foil+point-': 74, 'foil-point+': 5, 'foil-point-': 8}
- pointing = both actants, noun prompt: pointing hit 303/409 (74.1%); kappa(foil, pointing) = -0.007; cells {'foil+point+': 293, 'foil+point-': 103, 'foil-point+': 10, 'foil-point-': 3}
- kappa(foil, blind) = 0.076; cells {'foil+point+': 279, 'foil+point-': 117, 'foil-point+': 4, 'foil-point-': 9}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.78, blind=+1.24; intercept=+2.37; fit acc 0.968 vs majority 0.968
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+1.48, blind=+1.27; intercept=+1.72; fit acc 0.968 vs majority 0.968

### Agreement, all items, foil outcome = yes_correct (n=933)

- pointing = both actants, role prompt: pointing hit 381/933 (40.8%); kappa(foil, pointing) = 0.028; cells {'foil+point+': 360, 'foil+point-': 503, 'foil-point+': 21, 'foil-point-': 49}
- pointing = agent only, role prompt: pointing hit 664/933 (71.2%); kappa(foil, pointing) = 0.039; cells {'foil+point+': 620, 'foil+point-': 243, 'foil-point+': 44, 'foil-point-': 26}
- pointing = both actants, noun prompt: pointing hit 486/933 (52.1%); kappa(foil, pointing) = 0.020; cells {'foil+point+': 454, 'foil+point-': 409, 'foil-point+': 32, 'foil-point-': 38}
- kappa(foil, blind) = 0.061; cells {'foil+point+': 635, 'foil+point-': 228, 'foil-point+': 42, 'foil-point-': 28}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.49, blind=+0.59; intercept=+1.94; fit acc 0.925 vs majority 0.925
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.44, blind=+0.61; intercept=+1.80; fit acc 0.925 vs majority 0.925

### Agreement, detector-verified gold only, foil outcome = yes_correct (n=409)

- pointing = both actants, role prompt: pointing hit 228/409 (55.7%); kappa(foil, pointing) = 0.036; cells {'foil+point+': 214, 'foil+point-': 164, 'foil-point+': 14, 'foil-point-': 17}
- pointing = agent only, role prompt: pointing hit 327/409 (80.0%); kappa(foil, pointing) = 0.055; cells {'foil+point+': 305, 'foil+point-': 73, 'foil-point+': 22, 'foil-point-': 9}
- pointing = both actants, noun prompt: pointing hit 303/409 (74.1%); kappa(foil, pointing) = -0.067; cells {'foil+point+': 276, 'foil+point-': 102, 'foil-point+': 27, 'foil-point-': 4}
- kappa(foil, blind) = 0.065; cells {'foil+point+': 266, 'foil+point-': 112, 'foil-point+': 17, 'foil-point-': 14}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.39, blind=+0.58; intercept=+1.93; fit acc 0.924 vs majority 0.924
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.46, blind=+0.59; intercept=+1.77; fit acc 0.924 vs majority 0.924

## action-replacement (630 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 576/630 (91.4%) |
| pairwise, order-debiased | 593/630 (94.1%) |
| blind pairwise (no image) | 403/630 (64.0%) |
| mean P(yes) caption / foil | 0.632 / 0.140 |

- agent pointing, role_prompt: IoU>=0.5 470/630 (74.6%), mean IoU 0.703
- agent pointing, noun_prompt: IoU>=0.5 482/630 (76.5%), mean IoU 0.722
- kappa(foil, agent pointing) = -0.004; cells {'foil+point+': 442, 'foil+point-': 151, 'foil-point+': 28, 'foil-point-': 9}
- kappa(foil, blind) = 0.056; cells {'foil+point+': 386, 'foil+point-': 207, 'foil-point+': 17, 'foil-point-': 20}
- logistic: foil_correct ~ pointing + blind: coef: pointing=-0.07, blind=+0.71; intercept=+2.43; fit acc 0.941 vs majority 0.941

## aro-relation (1228 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 1177/1228 (95.8%) |
| pairwise, order-debiased | 1183/1228 (96.3%) |
| blind pairwise (no image) | 1123/1228 (91.4%) |
| mean P(yes) caption / foil | 0.818 / 0.136 |
| yes-rate (P(yes)>0.5) caption / foil | 0.846 / 0.099 |
| pairwise on the benchmark crop | 1185/1228 (96.5%) |

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| other-actant | noun_prompt | 1913/2456 (77.9%) | 2188/2456 (89.1%) | 0.739 | 1 |
| other-actant | role_prompt | 1291/2456 (52.6%) | 1847/2456 (75.2%) | 0.528 | 0 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 2456, full_image_box 0.281, image_center_point 0.634, largest_role_box 0.601, other_actant_box 0.202, random_box 0.021
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): 
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 2456, full_image_box 0.281, image_center_point 0.634, largest_role_box 0.601, other_actant_box 0.202, random_box 0.021

Both actants hit with role prompts, by role pair (top 8): object-subject 420/1228

### Agreement, all items, foil outcome = pair_correct (n=1228)

- pointing = both actants, role prompt: pointing hit 420/1228 (34.2%); kappa(foil, pointing) = 0.026; cells {'foil+point+': 415, 'foil+point-': 768, 'foil-point+': 5, 'foil-point-': 40}
- pointing = agent only, role prompt: pointing hit 0/1228 (0.0%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 0, 'foil+point-': 1183, 'foil-point+': 0, 'foil-point-': 45}
- pointing = both actants, noun prompt: pointing hit 753/1228 (61.3%); kappa(foil, pointing) = 0.027; cells {'foil+point+': 732, 'foil+point-': 451, 'foil-point+': 21, 'foil-point-': 24}
- kappa(foil, blind) = 0.227; cells {'foil+point+': 1098, 'foil+point-': 85, 'foil-point+': 25, 'foil-point-': 20}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+1.23, blind=+2.12; intercept=+1.29; fit acc 0.963 vs majority 0.963
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+2.12; intercept=+1.58; fit acc 0.963 vs majority 0.963

### Agreement, all items, foil outcome = yes_correct (n=1228)

- pointing = both actants, role prompt: pointing hit 420/1228 (34.2%); kappa(foil, pointing) = 0.019; cells {'foil+point+': 410, 'foil+point-': 767, 'foil-point+': 10, 'foil-point-': 41}
- pointing = agent only, role prompt: pointing hit 0/1228 (0.0%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 0, 'foil+point-': 1177, 'foil-point+': 0, 'foil-point-': 51}
- pointing = both actants, noun prompt: pointing hit 753/1228 (61.3%); kappa(foil, pointing) = 0.013; cells {'foil+point+': 725, 'foil+point-': 452, 'foil-point+': 28, 'foil-point-': 23}
- kappa(foil, blind) = 0.199; cells {'foil+point+': 1091, 'foil+point-': 86, 'foil-point+': 32, 'foil-point-': 19}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.70, blind=+1.84; intercept=+1.44; fit acc 0.958 vs majority 0.958
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+1.84; intercept=+1.63; fit acc 0.958 vs majority 0.958

## aro-spatial (300 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 244/300 (81.3%) |
| pairwise, order-debiased | 245/300 (81.7%) |
| blind pairwise (no image) | 157/300 (52.3%) |
| mean P(yes) caption / foil | 0.534 / 0.076 |
| yes-rate (P(yes)>0.5) caption / foil | 0.520 / 0.047 |
| pairwise on the benchmark crop | 276/300 (92.0%) |

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| other-actant | noun_prompt | 346/600 (57.7%) | 417/600 (69.5%) | 0.560 | 0 |
| other-actant | role_prompt | 137/600 (22.8%) | 255/600 (42.5%) | 0.264 | 0 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 600, full_image_box 0.035, image_center_point 0.393, largest_role_box 0.500, other_actant_box 0.000, random_box 0.014
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): 
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 600, full_image_box 0.035, image_center_point 0.393, largest_role_box 0.500, other_actant_box 0.000, random_box 0.014

Both actants hit with role prompts, by role pair (top 8): object-subject 18/300

### Agreement, all items, foil outcome = pair_correct (n=300)

- pointing = both actants, role prompt: pointing hit 18/300 (6.0%); kappa(foil, pointing) = -0.006; cells {'foil+point+': 14, 'foil+point-': 231, 'foil-point+': 4, 'foil-point-': 51}
- pointing = agent only, role prompt: pointing hit 0/300 (0.0%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 0, 'foil+point-': 245, 'foil-point+': 0, 'foil-point-': 55}
- pointing = both actants, noun prompt: pointing hit 102/300 (34.0%); kappa(foil, pointing) = 0.185; cells {'foil+point+': 100, 'foil+point-': 145, 'foil-point+': 2, 'foil-point-': 53}
- kappa(foil, blind) = 0.052; cells {'foil+point+': 132, 'foil+point-': 113, 'foil-point+': 25, 'foil-point-': 30}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=-0.15, blind=+0.30; intercept=+1.35; fit acc 0.817 vs majority 0.817
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+0.31; intercept=+1.34; fit acc 0.817 vs majority 0.817

### Agreement, all items, foil outcome = yes_correct (n=300)

- pointing = both actants, role prompt: pointing hit 18/300 (6.0%); kappa(foil, pointing) = -0.006; cells {'foil+point+': 14, 'foil+point-': 230, 'foil-point+': 4, 'foil-point-': 52}
- pointing = agent only, role prompt: pointing hit 0/300 (0.0%); kappa(foil, pointing) = 0.000; cells {'foil+point+': 0, 'foil+point-': 244, 'foil-point+': 0, 'foil-point-': 56}
- pointing = both actants, noun prompt: pointing hit 102/300 (34.0%); kappa(foil, pointing) = 0.145; cells {'foil+point+': 96, 'foil+point-': 148, 'foil-point+': 6, 'foil-point-': 50}
- kappa(foil, blind) = 0.004; cells {'foil+point+': 128, 'foil+point-': 116, 'foil-point+': 29, 'foil-point-': 27}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=-0.17, blind=+0.02; intercept=+1.47; fit acc 0.813 vs majority 0.813
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+0.02; intercept=+1.46; fit acc 0.813 vs majority 0.813

## controls, actant-swap (933 items, 1866 role targets)

- text-only role resolution correct: 1635/1866 (87.6%) (agent 849/895 (94.9%), other 786/971 (80.9%))
- pointing hit, role prompt: unconditioned 1195/1866 (64.0%) | caption-conditioned 1324/1866 (71.0%) | noun prompt 1356/1866 (72.7%)
- caption-conditioned by target: agent 699/895 (78.1%), other 625/971 (64.4%)
- both participants by role: unconditioned 381/933 (40.8%) | conditioned 466/933 (49.9%)
- text resolved correctly but unconditioned pointing failed: 556/1635 (34.0%) of text-correct targets
- conflict pointing (foil caption in prompt), non-nested targets n=1666: image-consistent 991/1666 (59.5%), text-following 238/1666 (14.3%), both 9/1666 (0.5%), neither 428/1666 (25.7%); nested pairs excluded: 200

## controls, aro-relation (1228 items, 2456 role targets)

- text-only role resolution correct: 2139/2456 (87.1%) (agent n/a, other 2139/2456 (87.1%))
- pointing hit, role prompt: unconditioned 1294/2456 (52.7%) | caption-conditioned 1842/2456 (75.0%) | noun prompt 1913/2456 (77.9%)
- caption-conditioned by target: agent n/a, other 1842/2456 (75.0%)
- both participants by role: unconditioned 424/1228 (34.5%) | conditioned 735/1228 (59.9%)
- text resolved correctly but unconditioned pointing failed: 1000/2139 (46.8%) of text-correct targets
- conflict pointing (foil caption in prompt), non-nested targets n=1960: image-consistent 1226/1960 (62.6%), text-following 266/1960 (13.6%), both 28/1960 (1.4%), neither 440/1960 (22.4%); nested pairs excluded: 496

## blind likelihood baseline, actant-swap (933 items)

- caption more likely than foil (text only): 90.4% | clearly text-solvable (margin > 1.0 nat): 84.8% | balanced: 9.0% | foil preferred: 6.2%
- stratum solvable (n=791): foil pass 96.5%, both-by-role 41.1%, P(point | foil pass) 41.7%, cells {'foil+point+': 318, 'foil+point-': 445, 'foil-point+': 7, 'foil-point-': 21}
- stratum balanced (n=84): foil pass 95.2%, both-by-role 44.0%, P(point | foil pass) 43.8%, cells {'foil+point+': 35, 'foil+point-': 45, 'foil-point+': 2, 'foil-point-': 2}
- stratum foil_preferred (n=58): foil pass 84.5%, both-by-role 32.8%, P(point | foil pass) 36.7%, cells {'foil+point+': 18, 'foil+point-': 31, 'foil-point+': 1, 'foil-point-': 8}

## blind likelihood baseline, action-replacement (630 items)

- caption more likely than foil (text only): 69.5% | clearly text-solvable (margin > 1.0 nat): 61.9% | balanced: 15.1% | foil preferred: 23.0%

## blind likelihood baseline, aro-relation (1228 items)

- caption more likely than foil (text only): 95.7% | clearly text-solvable (margin > 1.0 nat): 93.3% | balanced: 4.1% | foil preferred: 2.6%
- stratum solvable (n=1146): foil pass 98.1%, both-by-role 35.3%, P(point | foil pass) 35.7%, cells {'foil+point+': 401, 'foil+point-': 723, 'foil-point+': 3, 'foil-point-': 19}
- stratum balanced (n=51): foil pass 74.5%, both-by-role 17.6%, P(point | foil pass) 18.4%, cells {'foil+point+': 7, 'foil+point-': 31, 'foil-point+': 2, 'foil-point-': 11}
- stratum foil_preferred (n=31): foil pass 67.7%, both-by-role 22.6%, P(point | foil pass) 33.3%, cells {'foil+point+': 7, 'foil+point-': 14, 'foil-point+': 0, 'foil-point-': 10}

## blind likelihood baseline, aro-spatial (300 items)

- caption more likely than foil (text only): 49.7% | clearly text-solvable (margin > 1.0 nat): 31.0% | balanced: 36.3% | foil preferred: 32.7%
- stratum solvable (n=93): foil pass 79.6%, both-by-role 4.3%, P(point | foil pass) 4.1%, cells {'foil+point+': 3, 'foil+point-': 71, 'foil-point+': 1, 'foil-point-': 18}
- stratum balanced (n=109): foil pass 84.4%, both-by-role 3.7%, P(point | foil pass) 4.3%, cells {'foil+point+': 4, 'foil+point-': 88, 'foil-point+': 0, 'foil-point-': 17}
- stratum foil_preferred (n=98): foil pass 80.6%, both-by-role 10.2%, P(point | foil pass) 8.9%, cells {'foil+point+': 7, 'foil+point-': 72, 'foil-point+': 3, 'foil-point-': 16}

