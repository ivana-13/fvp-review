# Summary for qwen3vl-4b

Gold check available: 409 of 933 checked actant-swap items have both actant boxes confirmed by Grounding DINO.

## actant-swap (933 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 814/933 (87.2%) |
| pairwise, order-debiased | 883/933 (94.6%) |
| blind pairwise (no image) | 125/933 (13.4%) |
| mean P(yes) caption / foil | 0.501 / 0.047 |
| yes-rate (P(yes)>0.5) caption / foil | 0.508 / 0.039 |

Verb naming: strict 221/933 (23.7%), WordNet-synonym 260/933 (27.9%)

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| agent | noun_prompt | 735/895 (82.1%) | 851/895 (95.1%) | 0.797 | 18 |
| agent | role_prompt | 704/895 (78.7%) | 836/895 (93.4%) | 0.771 | 10 |
| other-actant | noun_prompt | 708/971 (72.9%) | 887/971 (91.3%) | 0.699 | 16 |
| other-actant | role_prompt | 573/971 (59.0%) | 804/971 (82.8%) | 0.584 | 51 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 1866, full_image_box 0.311, image_center_point 0.671, largest_role_box 0.554, other_actant_box 0.107, random_box 0.020
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): n_targets 895, full_image_box 0.352, image_center_point 0.769, largest_role_box 0.639, other_actant_box 0.107, random_box 0.026
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 971, full_image_box 0.273, image_center_point 0.582, largest_role_box 0.475, other_actant_box 0.107, random_box 0.018

Both actants hit with role prompts, by role pair (top 8): agent-item 110/202; agent-victim 42/66; agent-vehicle 15/54; agent-target 14/52; agent-tool 21/48; agent-destination 4/38; agent-student 14/37; agent-contact 22/31

### Agreement, all items, foil outcome = pair_correct (n=933)

- pointing = both actants, role prompt: pointing hit 423/933 (45.3%); kappa(foil, pointing) = 0.034; cells {'foil+point+': 409, 'foil+point-': 474, 'foil-point+': 14, 'foil-point-': 36}
- pointing = agent only, role prompt: pointing hit 704/933 (75.5%); kappa(foil, pointing) = 0.045; cells {'foil+point+': 672, 'foil+point-': 211, 'foil-point+': 32, 'foil-point-': 18}
- pointing = both actants, noun prompt: pointing hit 563/933 (60.3%); kappa(foil, pointing) = 0.017; cells {'foil+point+': 536, 'foil+point-': 347, 'foil-point+': 27, 'foil-point-': 23}
- kappa(foil, blind) = -0.019; cells {'foil+point+': 111, 'foil+point-': 772, 'foil-point+': 14, 'foil-point-': 36}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.75, blind=-0.93; intercept=+2.76; fit acc 0.946 vs majority 0.946
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.54, blind=-0.90; intercept=+2.66; fit acc 0.946 vs majority 0.946

### Agreement, detector-verified gold only, foil outcome = pair_correct (n=409)

- pointing = both actants, role prompt: pointing hit 258/409 (63.1%); kappa(foil, pointing) = 0.086; cells {'foil+point+': 249, 'foil+point-': 135, 'foil-point+': 9, 'foil-point-': 16}
- pointing = agent only, role prompt: pointing hit 348/409 (85.1%); kappa(foil, pointing) = 0.083; cells {'foil+point+': 330, 'foil+point-': 54, 'foil-point+': 18, 'foil-point-': 7}
- pointing = both actants, noun prompt: pointing hit 358/409 (87.5%); kappa(foil, pointing) = -0.003; cells {'foil+point+': 336, 'foil+point-': 48, 'foil-point+': 22, 'foil-point-': 3}
- kappa(foil, blind) = -0.022; cells {'foil+point+': 48, 'foil+point-': 336, 'foil-point+': 7, 'foil-point-': 18}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+1.05, blind=-0.89; intercept=+2.34; fit acc 0.939 vs majority 0.939
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.70, blind=-0.81; intercept=+2.31; fit acc 0.939 vs majority 0.939

### Agreement, all items, foil outcome = yes_correct (n=933)

- pointing = both actants, role prompt: pointing hit 423/933 (45.3%); kappa(foil, pointing) = 0.076; cells {'foil+point+': 388, 'foil+point-': 426, 'foil-point+': 35, 'foil-point-': 84}
- pointing = agent only, role prompt: pointing hit 704/933 (75.5%); kappa(foil, pointing) = 0.088; cells {'foil+point+': 627, 'foil+point-': 187, 'foil-point+': 77, 'foil-point-': 42}
- pointing = both actants, noun prompt: pointing hit 563/933 (60.3%); kappa(foil, pointing) = 0.095; cells {'foil+point+': 510, 'foil+point-': 304, 'foil-point+': 53, 'foil-point-': 66}
- kappa(foil, blind) = -0.017; cells {'foil+point+': 103, 'foil+point-': 711, 'foil-point+': 22, 'foil-point-': 97}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.76, blind=-0.45; intercept=+1.70; fit acc 0.872 vs majority 0.872
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.58, blind=-0.43; intercept=+1.57; fit acc 0.872 vs majority 0.872

### Agreement, detector-verified gold only, foil outcome = yes_correct (n=409)

- pointing = both actants, role prompt: pointing hit 258/409 (63.1%); kappa(foil, pointing) = 0.107; cells {'foil+point+': 234, 'foil+point-': 123, 'foil-point+': 24, 'foil-point-': 28}
- pointing = agent only, role prompt: pointing hit 348/409 (85.1%); kappa(foil, pointing) = 0.087; cells {'foil+point+': 308, 'foil+point-': 49, 'foil-point+': 40, 'foil-point-': 12}
- pointing = both actants, noun prompt: pointing hit 358/409 (87.5%); kappa(foil, pointing) = 0.100; cells {'foil+point+': 317, 'foil+point-': 40, 'foil-point+': 41, 'foil-point-': 11}
- kappa(foil, blind) = -0.019; cells {'foil+point+': 45, 'foil+point-': 312, 'foil-point+': 10, 'foil-point-': 42}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.75, blind=-0.49; intercept=+1.58; fit acc 0.873 vs majority 0.873
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.55, blind=-0.43; intercept=+1.54; fit acc 0.873 vs majority 0.873

## action-replacement (630 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 577/630 (91.6%) |
| pairwise, order-debiased | 601/630 (95.4%) |
| blind pairwise (no image) | 225/630 (35.7%) |
| mean P(yes) caption / foil | 0.492 / 0.048 |

- agent pointing, role_prompt: IoU>=0.5 490/630 (77.8%), mean IoU 0.761
- agent pointing, noun_prompt: IoU>=0.5 499/630 (79.2%), mean IoU 0.758
- kappa(foil, agent pointing) = 0.033; cells {'foil+point+': 470, 'foil+point-': 131, 'foil-point+': 20, 'foil-point-': 9}
- kappa(foil, blind) = -0.018; cells {'foil+point+': 211, 'foil+point-': 390, 'foil-point+': 14, 'foil-point-': 15}
- logistic: foil_correct ~ pointing + blind: coef: pointing=+0.40, blind=-0.47; intercept=+2.92; fit acc 0.954 vs majority 0.954

## aro-relation (1228 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 1158/1228 (94.3%) |
| pairwise, order-debiased | 1197/1228 (97.5%) |
| blind pairwise (no image) | 79/1228 (6.4%) |
| mean P(yes) caption / foil | 0.820 / 0.087 |
| yes-rate (P(yes)>0.5) caption / foil | 0.828 / 0.071 |
| pairwise on the benchmark crop | 1198/1228 (97.6%) |

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| other-actant | noun_prompt | 2155/2456 (87.7%) | 2333/2456 (95.0%) | 0.818 | 8 |
| other-actant | role_prompt | 1522/2456 (62.0%) | 1939/2456 (78.9%) | 0.611 | 2 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 2456, full_image_box 0.281, image_center_point 0.634, largest_role_box 0.601, other_actant_box 0.202, random_box 0.021
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): 
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 2456, full_image_box 0.281, image_center_point 0.634, largest_role_box 0.601, other_actant_box 0.202, random_box 0.021

Both actants hit with role prompts, by role pair (top 8): object-subject 511/1228

### Agreement, all items, foil outcome = pair_correct (n=1228)

- pointing = both actants, role prompt: pointing hit 511/1228 (41.6%); kappa(foil, pointing) = 0.017; cells {'foil+point+': 504, 'foil+point-': 693, 'foil-point+': 7, 'foil-point-': 24}
- pointing = agent only, role prompt: pointing hit 0/1228 (0.0%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 0, 'foil+point-': 1197, 'foil-point+': 0, 'foil-point-': 31}
- pointing = both actants, noun prompt: pointing hit 965/1228 (78.6%); kappa(foil, pointing) = -0.005; cells {'foil+point+': 940, 'foil+point-': 257, 'foil-point+': 25, 'foil-point-': 6}
- kappa(foil, blind) = -0.027; cells {'foil+point+': 62, 'foil+point-': 1135, 'foil-point+': 17, 'foil-point-': 14}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.51, blind=-2.63; intercept=+4.03; fit acc 0.975 vs majority 0.975
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=-2.70; intercept=+4.21; fit acc 0.975 vs majority 0.975

### Agreement, all items, foil outcome = yes_correct (n=1228)

- pointing = both actants, role prompt: pointing hit 511/1228 (41.6%); kappa(foil, pointing) = 0.029; cells {'foil+point+': 492, 'foil+point-': 666, 'foil-point+': 19, 'foil-point-': 51}
- pointing = agent only, role prompt: pointing hit 0/1228 (0.0%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 0, 'foil+point-': 1158, 'foil-point+': 0, 'foil-point-': 70}
- pointing = both actants, noun prompt: pointing hit 965/1228 (78.6%); kappa(foil, pointing) = 0.013; cells {'foil+point+': 912, 'foil+point-': 246, 'foil-point+': 53, 'foil-point-': 17}
- kappa(foil, blind) = -0.023; cells {'foil+point+': 62, 'foil+point-': 1096, 'foil-point+': 17, 'foil-point-': 53}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.53, blind=-1.50; intercept=+2.80; fit acc 0.943 vs majority 0.943
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=-1.57; intercept=+3.00; fit acc 0.943 vs majority 0.943

## aro-spatial (300 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 243/300 (81.0%) |
| pairwise, order-debiased | 239/300 (79.7%) |
| blind pairwise (no image) | 130/300 (43.3%) |
| mean P(yes) caption / foil | 0.570 / 0.084 |
| yes-rate (P(yes)>0.5) caption / foil | 0.563 / 0.073 |
| pairwise on the benchmark crop | 263/300 (87.7%) |

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| other-actant | noun_prompt | 423/600 (70.5%) | 492/600 (82.0%) | 0.666 | 7 |
| other-actant | role_prompt | 168/600 (28.0%) | 290/600 (48.3%) | 0.314 | 0 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 600, full_image_box 0.035, image_center_point 0.393, largest_role_box 0.500, other_actant_box 0.000, random_box 0.014
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): 
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 600, full_image_box 0.035, image_center_point 0.393, largest_role_box 0.500, other_actant_box 0.000, random_box 0.014

Both actants hit with role prompts, by role pair (top 8): object-subject 27/300

### Agreement, all items, foil outcome = pair_correct (n=300)

- pointing = both actants, role prompt: pointing hit 27/300 (9.0%); kappa(foil, pointing) = -0.005; cells {'foil+point+': 21, 'foil+point-': 218, 'foil-point+': 6, 'foil-point-': 55}
- pointing = agent only, role prompt: pointing hit 0/300 (0.0%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 0, 'foil+point-': 239, 'foil-point+': 0, 'foil-point-': 61}
- pointing = both actants, noun prompt: pointing hit 151/300 (50.3%); kappa(foil, pointing) = 0.103; cells {'foil+point+': 128, 'foil+point-': 111, 'foil-point+': 23, 'foil-point-': 38}
- kappa(foil, blind) = 0.079; cells {'foil+point+': 110, 'foil+point-': 129, 'foil-point+': 20, 'foil-point-': 41}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=-0.07, blind=+0.51; intercept=+1.17; fit acc 0.797 vs majority 0.797
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+0.51; intercept=+1.16; fit acc 0.797 vs majority 0.797

### Agreement, all items, foil outcome = yes_correct (n=300)

- pointing = both actants, role prompt: pointing hit 27/300 (9.0%); kappa(foil, pointing) = -0.025; cells {'foil+point+': 19, 'foil+point-': 224, 'foil-point+': 8, 'foil-point-': 49}
- pointing = agent only, role prompt: pointing hit 0/300 (0.0%); kappa(foil, pointing) = 0.000; cells {'foil+point+': 0, 'foil+point-': 243, 'foil-point+': 0, 'foil-point-': 57}
- pointing = both actants, noun prompt: pointing hit 151/300 (50.3%); kappa(foil, pointing) = 0.103; cells {'foil+point+': 130, 'foil+point-': 113, 'foil-point+': 21, 'foil-point-': 36}
- kappa(foil, blind) = 0.083; cells {'foil+point+': 112, 'foil+point-': 131, 'foil-point+': 18, 'foil-point-': 39}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=-0.52, blind=+0.55; intercept=+1.29; fit acc 0.810 vs majority 0.810
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+0.56; intercept=+1.23; fit acc 0.810 vs majority 0.810

## controls, actant-swap (933 items, 1866 role targets)

- text-only role resolution correct: 1730/1866 (92.7%) (agent 849/895 (94.9%), other 881/971 (90.7%))
- pointing hit, role prompt: unconditioned 1277/1866 (68.4%) | caption-conditioned 1348/1866 (72.2%) | noun prompt 1443/1866 (77.3%)
- caption-conditioned by target: agent 734/895 (82.0%), other 614/971 (63.2%)
- both participants by role: unconditioned 423/933 (45.3%) | conditioned 481/933 (51.6%)
- text resolved correctly but unconditioned pointing failed: 532/1730 (30.8%) of text-correct targets
- conflict pointing (foil caption in prompt), non-nested targets n=1666: image-consistent 1033/1666 (62.0%), text-following 265/1666 (15.9%), both 10/1666 (0.6%), neither 358/1666 (21.5%); nested pairs excluded: 200

## controls, aro-relation (1228 items, 2456 role targets)

- text-only role resolution correct: 1841/2456 (75.0%) (agent n/a, other 1841/2456 (75.0%))
- pointing hit, role prompt: unconditioned 1525/2456 (62.1%) | caption-conditioned 1775/2456 (72.3%) | noun prompt 2155/2456 (87.7%)
- caption-conditioned by target: agent n/a, other 1775/2456 (72.3%)
- both participants by role: unconditioned 514/1228 (41.9%) | conditioned 656/1228 (53.4%)
- text resolved correctly but unconditioned pointing failed: 648/1841 (35.2%) of text-correct targets
- conflict pointing (foil caption in prompt), non-nested targets n=1960: image-consistent 1253/1960 (63.9%), text-following 356/1960 (18.2%), both 39/1960 (2.0%), neither 312/1960 (15.9%); nested pairs excluded: 496

## blind likelihood baseline, actant-swap (933 items)

- caption more likely than foil (text only): 89.8% | clearly text-solvable (margin > 1.0 nat): 85.0% | balanced: 7.3% | foil preferred: 7.7%
- stratum solvable (n=793): foil pass 95.8%, both-by-role 45.0%, P(point | foil pass) 46.1%, cells {'foil+point+': 350, 'foil+point-': 410, 'foil-point+': 7, 'foil-point-': 26}
- stratum balanced (n=68): foil pass 86.8%, both-by-role 50.0%, P(point | foil pass) 52.5%, cells {'foil+point+': 31, 'foil+point-': 28, 'foil-point+': 3, 'foil-point-': 6}
- stratum foil_preferred (n=72): foil pass 88.9%, both-by-role 44.4%, P(point | foil pass) 43.8%, cells {'foil+point+': 28, 'foil+point-': 36, 'foil-point+': 4, 'foil-point-': 4}

## blind likelihood baseline, action-replacement (630 items)

- caption more likely than foil (text only): 70.6% | clearly text-solvable (margin > 1.0 nat): 62.4% | balanced: 14.3% | foil preferred: 23.3%

## blind likelihood baseline, aro-relation (1228 items)

- caption more likely than foil (text only): 95.0% | clearly text-solvable (margin > 1.0 nat): 92.2% | balanced: 4.3% | foil preferred: 3.5%
- stratum solvable (n=1132): foil pass 99.3%, both-by-role 42.8%, P(point | foil pass) 42.8%, cells {'foil+point+': 481, 'foil+point-': 643, 'foil-point+': 4, 'foil-point-': 4}
- stratum balanced (n=56): foil pass 75.0%, both-by-role 35.7%, P(point | foil pass) 40.5%, cells {'foil+point+': 17, 'foil+point-': 25, 'foil-point+': 3, 'foil-point-': 11}
- stratum foil_preferred (n=40): foil pass 77.5%, both-by-role 15.0%, P(point | foil pass) 19.4%, cells {'foil+point+': 6, 'foil+point-': 25, 'foil-point+': 0, 'foil-point-': 9}

## blind likelihood baseline, aro-spatial (300 items)

- caption more likely than foil (text only): 52.3% | clearly text-solvable (margin > 1.0 nat): 30.7% | balanced: 36.0% | foil preferred: 33.3%
- stratum solvable (n=92): foil pass 75.0%, both-by-role 7.6%, P(point | foil pass) 8.7%, cells {'foil+point+': 6, 'foil+point-': 63, 'foil-point+': 1, 'foil-point-': 22}
- stratum balanced (n=108): foil pass 88.9%, both-by-role 12.0%, P(point | foil pass) 10.4%, cells {'foil+point+': 10, 'foil+point-': 86, 'foil-point+': 3, 'foil-point-': 9}
- stratum foil_preferred (n=100): foil pass 74.0%, both-by-role 7.0%, P(point | foil pass) 6.8%, cells {'foil+point+': 5, 'foil+point-': 69, 'foil-point+': 2, 'foil-point-': 24}

