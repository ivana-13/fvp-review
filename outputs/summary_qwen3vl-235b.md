# Summary for qwen3vl-235b

Gold check available: 409 of 933 checked actant-swap items have both actant boxes confirmed by Grounding DINO.

## actant-swap (933 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 882/933 (94.5%) |
| pairwise, order-debiased | 914/933 (98.0%) |
| blind pairwise (no image) | 838/933 (89.8%) |
| mean P(yes) caption / foil | 0.599 / 0.039 |
| yes-rate (P(yes)>0.5) caption / foil | 0.597 / 0.033 |

Verb naming: strict 291/933 (31.2%), WordNet-synonym 334/933 (35.8%)

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| agent | noun_prompt | 749/895 (83.7%) | 855/895 (95.5%) | 0.809 | 10 |
| agent | role_prompt | 722/895 (80.7%) | 846/895 (94.5%) | 0.788 | 12 |
| other-actant | noun_prompt | 716/971 (73.7%) | 889/971 (91.6%) | 0.708 | 19 |
| other-actant | role_prompt | 627/971 (64.6%) | 838/971 (86.3%) | 0.636 | 47 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 1866, full_image_box 0.311, image_center_point 0.671, largest_role_box 0.554, other_actant_box 0.107, random_box 0.020
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): n_targets 895, full_image_box 0.352, image_center_point 0.769, largest_role_box 0.639, other_actant_box 0.107, random_box 0.026
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 971, full_image_box 0.273, image_center_point 0.582, largest_role_box 0.475, other_actant_box 0.107, random_box 0.018

Both actants hit with role prompts, by role pair (top 8): agent-item 117/202; agent-victim 47/66; agent-vehicle 18/54; agent-target 25/52; agent-tool 27/48; agent-destination 5/38; agent-student 13/37; agent-contact 25/31

### Agreement, all items, foil outcome = pair_correct (n=933)

- pointing = both actants, role prompt: pointing hit 477/933 (51.1%); kappa(foil, pointing) = 0.025; cells {'foil+point+': 473, 'foil+point-': 441, 'foil-point+': 4, 'foil-point-': 15}
- pointing = agent only, role prompt: pointing hit 722/933 (77.4%); kappa(foil, pointing) = 0.052; cells {'foil+point+': 713, 'foil+point-': 201, 'foil-point+': 9, 'foil-point-': 10}
- pointing = both actants, noun prompt: pointing hit 585/933 (62.7%); kappa(foil, pointing) = 0.017; cells {'foil+point+': 576, 'foil+point-': 338, 'foil-point+': 9, 'foil-point-': 10}
- kappa(foil, blind) = 0.128; cells {'foil+point+': 828, 'foil+point-': 86, 'foil-point+': 10, 'foil-point-': 9}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+1.10, blind=+1.77; intercept=+2.06; fit acc 0.980 vs majority 0.980
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+1.14, blind=+1.78; intercept=+1.72; fit acc 0.980 vs majority 0.980

### Agreement, detector-verified gold only, foil outcome = pair_correct (n=409)

- pointing = both actants, role prompt: pointing hit 283/409 (69.2%); kappa(foil, pointing) = 0.060; cells {'foil+point+': 282, 'foil+point-': 120, 'foil-point+': 1, 'foil-point-': 6}
- pointing = agent only, role prompt: pointing hit 362/409 (88.5%); kappa(foil, pointing) = 0.084; cells {'foil+point+': 358, 'foil+point-': 44, 'foil-point+': 4, 'foil-point-': 3}
- pointing = both actants, noun prompt: pointing hit 372/409 (91.0%); kappa(foil, pointing) = -0.030; cells {'foil+point+': 365, 'foil+point-': 37, 'foil-point+': 7, 'foil-point-': 0}
- kappa(foil, blind) = 0.153; cells {'foil+point+': 358, 'foil+point-': 44, 'foil-point+': 2, 'foil-point-': 5}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+1.45, blind=+1.85; intercept=+1.92; fit acc 0.983 vs majority 0.983
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+1.06, blind=+1.84; intercept=+1.82; fit acc 0.983 vs majority 0.983

### Agreement, all items, foil outcome = yes_correct (n=933)

- pointing = both actants, role prompt: pointing hit 477/933 (51.1%); kappa(foil, pointing) = 0.035; cells {'foil+point+': 459, 'foil+point-': 423, 'foil-point+': 18, 'foil-point-': 33}
- pointing = agent only, role prompt: pointing hit 722/933 (77.4%); kappa(foil, pointing) = 0.113; cells {'foil+point+': 696, 'foil+point-': 186, 'foil-point+': 26, 'foil-point-': 25}
- pointing = both actants, noun prompt: pointing hit 585/933 (62.7%); kappa(foil, pointing) = 0.061; cells {'foil+point+': 564, 'foil+point-': 318, 'foil-point+': 21, 'foil-point-': 30}
- kappa(foil, blind) = 0.041; cells {'foil+point+': 795, 'foil+point-': 87, 'foil-point+': 43, 'foil-point-': 8}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.63, blind=+0.47; intercept=+2.16; fit acc 0.945 vs majority 0.945
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+1.18, blind=+0.47; intercept=+1.65; fit acc 0.945 vs majority 0.945

### Agreement, detector-verified gold only, foil outcome = yes_correct (n=409)

- pointing = both actants, role prompt: pointing hit 283/409 (69.2%); kappa(foil, pointing) = 0.037; cells {'foil+point+': 273, 'foil+point-': 118, 'foil-point+': 10, 'foil-point-': 8}
- pointing = agent only, role prompt: pointing hit 362/409 (88.5%); kappa(foil, pointing) = 0.129; cells {'foil+point+': 350, 'foil+point-': 41, 'foil-point+': 12, 'foil-point-': 6}
- pointing = both actants, noun prompt: pointing hit 372/409 (91.0%); kappa(foil, pointing) = 0.014; cells {'foil+point+': 356, 'foil+point-': 35, 'foil-point+': 16, 'foil-point-': 2}
- kappa(foil, blind) = 0.059; cells {'foil+point+': 346, 'foil+point-': 45, 'foil-point+': 14, 'foil-point-': 4}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.49, blind=+0.57; intercept=+2.28; fit acc 0.956 vs majority 0.956
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+1.11, blind=+0.55; intercept=+1.70; fit acc 0.956 vs majority 0.956

## action-replacement (630 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 585/630 (92.9%) |
| pairwise, order-debiased | 603/630 (95.7%) |
| blind pairwise (no image) | 410/630 (65.1%) |
| mean P(yes) caption / foil | 0.602 / 0.084 |

- agent pointing, role_prompt: IoU>=0.5 508/630 (80.6%), mean IoU 0.785
- agent pointing, noun_prompt: IoU>=0.5 503/630 (79.8%), mean IoU 0.767
- kappa(foil, agent pointing) = -0.018; cells {'foil+point+': 485, 'foil+point-': 118, 'foil-point+': 23, 'foil-point-': 4}
- kappa(foil, blind) = -0.013; cells {'foil+point+': 391, 'foil+point-': 212, 'foil-point+': 19, 'foil-point-': 8}
- logistic: foil_correct ~ pointing + blind: coef: pointing=-0.26, blind=-0.22; intercept=+3.47; fit acc 0.957 vs majority 0.957

## aro-relation (1228 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 1188/1228 (96.7%) |
| pairwise, order-debiased | 1200/1228 (97.7%) |
| blind pairwise (no image) | 1104/1228 (89.9%) |
| mean P(yes) caption / foil | 0.853 / 0.042 |
| yes-rate (P(yes)>0.5) caption / foil | 0.855 / 0.040 |
| pairwise on the benchmark crop | 1201/1228 (97.8%) |

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| other-actant | noun_prompt | 2162/2456 (88.0%) | 2317/2456 (94.3%) | 0.821 | 6 |
| other-actant | role_prompt | 1597/2456 (65.0%) | 1945/2456 (79.2%) | 0.629 | 3 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 2456, full_image_box 0.281, image_center_point 0.634, largest_role_box 0.601, other_actant_box 0.202, random_box 0.021
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): 
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 2456, full_image_box 0.281, image_center_point 0.634, largest_role_box 0.601, other_actant_box 0.202, random_box 0.021

Both actants hit with role prompts, by role pair (top 8): object-subject 567/1228

### Agreement, all items, foil outcome = pair_correct (n=1228)

- pointing = both actants, role prompt: pointing hit 567/1228 (46.2%); kappa(foil, pointing) = 0.036; cells {'foil+point+': 566, 'foil+point-': 634, 'foil-point+': 1, 'foil-point-': 27}
- pointing = agent only, role prompt: pointing hit 0/1228 (0.0%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 0, 'foil+point-': 1200, 'foil-point+': 0, 'foil-point-': 28}
- pointing = both actants, noun prompt: pointing hit 968/1228 (78.8%); kappa(foil, pointing) = 0.015; cells {'foil+point+': 948, 'foil+point-': 252, 'foil-point+': 20, 'foil-point-': 8}
- kappa(foil, blind) = 0.207; cells {'foil+point+': 1094, 'foil+point-': 106, 'foil-point+': 10, 'foil-point-': 18}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+2.03, blind=+2.57; intercept=+1.38; fit acc 0.977 vs majority 0.977
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+2.53; intercept=+1.95; fit acc 0.977 vs majority 0.977

### Agreement, all items, foil outcome = yes_correct (n=1228)

- pointing = both actants, role prompt: pointing hit 567/1228 (46.2%); kappa(foil, pointing) = 0.044; cells {'foil+point+': 563, 'foil+point-': 625, 'foil-point+': 4, 'foil-point-': 36}
- pointing = agent only, role prompt: pointing hit 0/1228 (0.0%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 0, 'foil+point-': 1188, 'foil-point+': 0, 'foil-point-': 40}
- pointing = both actants, noun prompt: pointing hit 968/1228 (78.8%); kappa(foil, pointing) = 0.046; cells {'foil+point+': 943, 'foil+point-': 245, 'foil-point+': 25, 'foil-point-': 15}
- kappa(foil, blind) = 0.102; cells {'foil+point+': 1076, 'foil+point-': 112, 'foil-point+': 28, 'foil-point-': 12}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+1.69, blind=+1.25; intercept=+1.86; fit acc 0.967 vs majority 0.967
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+1.25; intercept=+2.36; fit acc 0.967 vs majority 0.967

## aro-spatial (300 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 250/300 (83.3%) |
| pairwise, order-debiased | 249/300 (83.0%) |
| blind pairwise (no image) | 155/300 (51.7%) |
| mean P(yes) caption / foil | 0.616 / 0.070 |
| yes-rate (P(yes)>0.5) caption / foil | 0.630 / 0.063 |
| pairwise on the benchmark crop | 278/300 (92.7%) |

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| other-actant | noun_prompt | 426/600 (71.0%) | 494/600 (82.3%) | 0.673 | 9 |
| other-actant | role_prompt | 176/600 (29.3%) | 326/600 (54.3%) | 0.327 | 0 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 600, full_image_box 0.035, image_center_point 0.393, largest_role_box 0.500, other_actant_box 0.000, random_box 0.014
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): 
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 600, full_image_box 0.035, image_center_point 0.393, largest_role_box 0.500, other_actant_box 0.000, random_box 0.014

Both actants hit with role prompts, by role pair (top 8): object-subject 25/300

### Agreement, all items, foil outcome = pair_correct (n=300)

- pointing = both actants, role prompt: pointing hit 25/300 (8.3%); kappa(foil, pointing) = -0.006; cells {'foil+point+': 20, 'foil+point-': 229, 'foil-point+': 5, 'foil-point-': 46}
- pointing = agent only, role prompt: pointing hit 0/300 (0.0%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 0, 'foil+point-': 249, 'foil-point+': 0, 'foil-point-': 51}
- pointing = both actants, noun prompt: pointing hit 152/300 (50.7%); kappa(foil, pointing) = 0.159; cells {'foil+point+': 138, 'foil+point-': 111, 'foil-point+': 14, 'foil-point-': 37}
- kappa(foil, blind) = 0.032; cells {'foil+point+': 131, 'foil+point-': 118, 'foil-point+': 24, 'foil-point-': 27}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=-0.15, blind=+0.20; intercept=+1.50; fit acc 0.830 vs majority 0.830
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+0.20; intercept=+1.48; fit acc 0.830 vs majority 0.830

### Agreement, all items, foil outcome = yes_correct (n=300)

- pointing = both actants, role prompt: pointing hit 25/300 (8.3%); kappa(foil, pointing) = 0.001; cells {'foil+point+': 21, 'foil+point-': 229, 'foil-point+': 4, 'foil-point-': 46}
- pointing = agent only, role prompt: pointing hit 0/300 (0.0%); kappa(foil, pointing) = 0.000; cells {'foil+point+': 0, 'foil+point-': 250, 'foil-point+': 0, 'foil-point-': 50}
- pointing = both actants, noun prompt: pointing hit 152/300 (50.7%); kappa(foil, pointing) = 0.126; cells {'foil+point+': 136, 'foil+point-': 114, 'foil-point+': 16, 'foil-point-': 34}
- kappa(foil, blind) = 0.039; cells {'foil+point+': 132, 'foil+point-': 118, 'foil-point+': 23, 'foil-point-': 27}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.07, blind=+0.25; intercept=+1.48; fit acc 0.833 vs majority 0.833
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+0.25; intercept=+1.49; fit acc 0.833 vs majority 0.833

## controls, actant-swap (933 items, 1866 role targets)

- text-only role resolution correct: 1773/1866 (95.0%) (agent 849/895 (94.9%), other 924/971 (95.2%))
- pointing hit, role prompt: unconditioned 1349/1866 (72.3%) | caption-conditioned 1442/1866 (77.3%) | noun prompt 1465/1866 (78.5%)
- caption-conditioned by target: agent 756/895 (84.5%), other 686/971 (70.6%)
- both participants by role: unconditioned 477/933 (51.1%) | conditioned 554/933 (59.4%)
- text resolved correctly but unconditioned pointing failed: 492/1773 (27.7%) of text-correct targets
- conflict pointing (foil caption in prompt), non-nested targets n=1666: image-consistent 1009/1666 (60.6%), text-following 306/1666 (18.4%), both 14/1666 (0.8%), neither 337/1666 (20.2%); nested pairs excluded: 200

## controls, aro-relation (1228 items, 2456 role targets)

- text-only role resolution correct: 2273/2456 (92.5%) (agent n/a, other 2273/2456 (92.5%))
- pointing hit, role prompt: unconditioned 1594/2456 (64.9%) | caption-conditioned 2035/2456 (82.9%) | noun prompt 2162/2456 (88.0%)
- caption-conditioned by target: agent n/a, other 2035/2456 (82.9%)
- both participants by role: unconditioned 565/1228 (46.0%) | conditioned 865/1228 (70.4%)
- text resolved correctly but unconditioned pointing failed: 750/2273 (33.0%) of text-correct targets
- conflict pointing (foil caption in prompt), non-nested targets n=1960: image-consistent 1235/1960 (63.0%), text-following 403/1960 (20.6%), both 29/1960 (1.5%), neither 293/1960 (14.9%); nested pairs excluded: 496

## blind likelihood baseline, actant-swap (933 items)

- caption more likely than foil (text only): 91.0% | clearly text-solvable (margin > 1.0 nat): 87.0% | balanced: 7.0% | foil preferred: 6.0%
- stratum solvable (n=812): foil pass 98.8%, both-by-role 50.6%, P(point | foil pass) 51.1%, cells {'foil+point+': 410, 'foil+point-': 392, 'foil-point+': 1, 'foil-point-': 9}
- stratum balanced (n=65): foil pass 95.4%, both-by-role 58.5%, P(point | foil pass) 58.1%, cells {'foil+point+': 36, 'foil+point-': 26, 'foil-point+': 2, 'foil-point-': 1}
- stratum foil_preferred (n=56): foil pass 89.3%, both-by-role 50.0%, P(point | foil pass) 54.0%, cells {'foil+point+': 27, 'foil+point-': 23, 'foil-point+': 1, 'foil-point-': 5}

## blind likelihood baseline, action-replacement (630 items)

- caption more likely than foil (text only): 71.9% | clearly text-solvable (margin > 1.0 nat): 65.9% | balanced: 12.1% | foil preferred: 22.1%

## blind likelihood baseline, aro-relation (1228 items)

- caption more likely than foil (text only): 95.4% | clearly text-solvable (margin > 1.0 nat): 91.7% | balanced: 5.9% | foil preferred: 2.4%
- stratum solvable (n=1132): foil pass 99.6%, both-by-role 48.0%, P(point | foil pass) 48.1%, cells {'foil+point+': 543, 'foil+point-': 585, 'foil-point+': 0, 'foil-point-': 4}
- stratum balanced (n=67): foil pass 80.6%, both-by-role 28.4%, P(point | foil pass) 33.3%, cells {'foil+point+': 18, 'foil+point-': 36, 'foil-point+': 1, 'foil-point-': 12}
- stratum foil_preferred (n=29): foil pass 62.1%, both-by-role 17.2%, P(point | foil pass) 27.8%, cells {'foil+point+': 5, 'foil+point-': 13, 'foil-point+': 0, 'foil-point-': 11}

## blind likelihood baseline, aro-spatial (300 items)

- caption more likely than foil (text only): 49.3% | clearly text-solvable (margin > 1.0 nat): 27.0% | balanced: 44.7% | foil preferred: 28.3%
- stratum solvable (n=81): foil pass 81.5%, both-by-role 2.5%, P(point | foil pass) 1.5%, cells {'foil+point+': 1, 'foil+point-': 65, 'foil-point+': 1, 'foil-point-': 14}
- stratum balanced (n=134): foil pass 84.3%, both-by-role 12.7%, P(point | foil pass) 12.4%, cells {'foil+point+': 14, 'foil+point-': 99, 'foil-point+': 3, 'foil-point-': 18}
- stratum foil_preferred (n=85): foil pass 82.4%, both-by-role 7.1%, P(point | foil pass) 7.1%, cells {'foil+point+': 5, 'foil+point-': 65, 'foil-point+': 1, 'foil-point-': 14}

