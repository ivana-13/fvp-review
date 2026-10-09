# Summary for molmo-7b-d

Gold check available: 409 of 933 checked actant-swap items have both actant boxes confirmed by Grounding DINO.

## actant-swap (933 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 735/933 (78.8%) |
| pairwise, order-debiased | 849/933 (91.0%) |
| blind pairwise (no image) | 673/933 (72.1%) |
| mean P(yes) caption / foil | 0.372 / 0.146 |
| yes-rate (P(yes)>0.5) caption / foil | 0.309 / 0.033 |

Verb naming: strict 208/933 (22.3%), WordNet-synonym 230/933 (24.7%)

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| agent | noun_prompt | 816/895 (91.2%) | 816/895 (91.2%) | 0.912 | 895 |
| agent | role_prompt | 633/895 (70.7%) | 633/895 (70.7%) | 0.707 | 895 |
| other-actant | noun_prompt | 866/971 (89.2%) | 866/971 (89.2%) | 0.892 | 971 |
| other-actant | role_prompt | 653/971 (67.3%) | 653/971 (67.3%) | 0.673 | 971 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 1866, full_image_box 0.311, image_center_point 0.671, largest_role_box 0.554, other_actant_box 0.107, random_box 0.020
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): n_targets 895, full_image_box 0.352, image_center_point 0.769, largest_role_box 0.639, other_actant_box 0.107, random_box 0.026
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 971, full_image_box 0.273, image_center_point 0.582, largest_role_box 0.475, other_actant_box 0.107, random_box 0.018

Both actants hit with role prompts, by role pair (top 8): agent-item 98/202; agent-victim 48/66; agent-vehicle 25/54; agent-target 9/52; agent-tool 8/48; agent-destination 9/38; agent-student 31/37; agent-contact 17/31

### Agreement, all items, foil outcome = pair_correct (n=933)

- pointing = both actants, role prompt: pointing hit 461/933 (49.4%); kappa(foil, pointing) = 0.083; cells {'foil+point+': 439, 'foil+point-': 410, 'foil-point+': 22, 'foil-point-': 62}
- pointing = agent only, role prompt: pointing hit 633/933 (67.8%); kappa(foil, pointing) = 0.061; cells {'foil+point+': 586, 'foil+point-': 263, 'foil-point+': 47, 'foil-point-': 37}
- pointing = both actants, noun prompt: pointing hit 761/933 (81.6%); kappa(foil, pointing) = 0.085; cells {'foil+point+': 702, 'foil+point-': 147, 'foil-point+': 59, 'foil-point-': 25}
- kappa(foil, blind) = 0.105; cells {'foil+point+': 628, 'foil+point-': 221, 'foil-point+': 45, 'foil-point-': 39}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+1.05, blind=+0.88; intercept=+1.34; fit acc 0.910 vs majority 0.910
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.53, blind=+0.86; intercept=+1.42; fit acc 0.910 vs majority 0.910

### Agreement, detector-verified gold only, foil outcome = pair_correct (n=409)

- pointing = both actants, role prompt: pointing hit 212/409 (51.8%); kappa(foil, pointing) = 0.113; cells {'foil+point+': 204, 'foil+point-': 168, 'foil-point+': 8, 'foil-point-': 29}
- pointing = agent only, role prompt: pointing hit 265/409 (64.8%); kappa(foil, pointing) = 0.051; cells {'foil+point+': 245, 'foil+point-': 127, 'foil-point+': 20, 'foil-point-': 17}
- pointing = both actants, noun prompt: pointing hit 373/409 (91.2%); kappa(foil, pointing) = 0.052; cells {'foil+point+': 341, 'foil+point-': 31, 'foil-point+': 32, 'foil-point-': 5}
- kappa(foil, blind) = 0.158; cells {'foil+point+': 271, 'foil+point-': 101, 'foil-point+': 15, 'foil-point-': 22}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+1.37, blind=+1.32; intercept=+0.99; fit acc 0.910 vs majority 0.910
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.54, blind=+1.26; intercept=+1.24; fit acc 0.910 vs majority 0.910

### Agreement, all items, foil outcome = yes_correct (n=933)

- pointing = both actants, role prompt: pointing hit 461/933 (49.4%); kappa(foil, pointing) = 0.119; cells {'foil+point+': 391, 'foil+point-': 344, 'foil-point+': 70, 'foil-point-': 128}
- pointing = agent only, role prompt: pointing hit 633/933 (67.8%); kappa(foil, pointing) = 0.072; cells {'foil+point+': 512, 'foil+point-': 223, 'foil-point+': 121, 'foil-point-': 77}
- pointing = both actants, noun prompt: pointing hit 761/933 (81.6%); kappa(foil, pointing) = 0.118; cells {'foil+point+': 617, 'foil+point-': 118, 'foil-point+': 144, 'foil-point-': 54}
- kappa(foil, blind) = 0.068; cells {'foil+point+': 542, 'foil+point-': 193, 'foil-point+': 131, 'foil-point-': 67}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.72, blind=+0.36; intercept=+0.74; fit acc 0.788 vs majority 0.788
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.37, blind=+0.35; intercept=+0.82; fit acc 0.788 vs majority 0.788

### Agreement, detector-verified gold only, foil outcome = yes_correct (n=409)

- pointing = both actants, role prompt: pointing hit 212/409 (51.8%); kappa(foil, pointing) = 0.166; cells {'foil+point+': 184, 'foil+point-': 139, 'foil-point+': 28, 'foil-point-': 58}
- pointing = agent only, role prompt: pointing hit 265/409 (64.8%); kappa(foil, pointing) = 0.103; cells {'foil+point+': 218, 'foil+point-': 105, 'foil-point+': 47, 'foil-point-': 39}
- pointing = both actants, noun prompt: pointing hit 373/409 (91.2%); kappa(foil, pointing) = 0.120; cells {'foil+point+': 301, 'foil+point-': 22, 'foil-point+': 72, 'foil-point-': 14}
- kappa(foil, blind) = 0.103; cells {'foil+point+': 234, 'foil+point-': 89, 'foil-point+': 52, 'foil-point-': 34}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.98, blind=+0.58; intercept=+0.50; fit acc 0.790 vs majority 0.790
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.56, blind=+0.56; intercept=+0.61; fit acc 0.790 vs majority 0.790

## action-replacement (630 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 533/630 (84.6%) |
| pairwise, order-debiased | 562/630 (89.2%) |
| blind pairwise (no image) | 339/630 (53.8%) |
| mean P(yes) caption / foil | 0.381 / 0.141 |

- agent pointing, role_prompt: IoU>=0.5 443/630 (70.3%), mean IoU 0.703
- agent pointing, noun_prompt: IoU>=0.5 558/630 (88.6%), mean IoU 0.886
- kappa(foil, agent pointing) = 0.082; cells {'foil+point+': 404, 'foil+point-': 158, 'foil-point+': 39, 'foil-point-': 29}
- kappa(foil, blind) = 0.072; cells {'foil+point+': 313, 'foil+point-': 249, 'foil-point+': 26, 'foil-point-': 42}
- logistic: foil_correct ~ pointing + blind: coef: pointing=+0.60, blind=+0.67; intercept=+1.40; fit acc 0.892 vs majority 0.892

## aro-relation (1228 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 1092/1228 (88.9%) |
| pairwise, order-debiased | 1180/1228 (96.1%) |
| blind pairwise (no image) | 1062/1228 (86.5%) |
| mean P(yes) caption / foil | 0.454 / 0.134 |
| yes-rate (P(yes)>0.5) caption / foil | 0.409 / 0.014 |
| pairwise on the benchmark crop | 1187/1228 (96.7%) |

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| other-actant | noun_prompt | 2286/2456 (93.1%) | 2286/2456 (93.1%) | 0.931 | 2456 |
| other-actant | role_prompt | 1805/2456 (73.5%) | 1805/2456 (73.5%) | 0.735 | 2456 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 2456, full_image_box 0.281, image_center_point 0.634, largest_role_box 0.601, other_actant_box 0.202, random_box 0.021
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): 
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 2456, full_image_box 0.281, image_center_point 0.634, largest_role_box 0.601, other_actant_box 0.202, random_box 0.021

Both actants hit with role prompts, by role pair (top 8): object-subject 692/1228

### Agreement, all items, foil outcome = pair_correct (n=1228)

- pointing = both actants, role prompt: pointing hit 692/1228 (56.4%); kappa(foil, pointing) = 0.022; cells {'foil+point+': 671, 'foil+point-': 509, 'foil-point+': 21, 'foil-point-': 27}
- pointing = agent only, role prompt: pointing hit 0/1228 (0.0%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 0, 'foil+point-': 1180, 'foil-point+': 0, 'foil-point-': 48}
- pointing = both actants, noun prompt: pointing hit 1068/1228 (87.0%); kappa(foil, pointing) = 0.008; cells {'foil+point+': 1027, 'foil+point-': 153, 'foil-point+': 41, 'foil-point-': 7}
- kappa(foil, blind) = 0.164; cells {'foil+point+': 1037, 'foil+point-': 143, 'foil-point+': 25, 'foil-point-': 23}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.61, blind=+1.80; intercept=+1.56; fit acc 0.961 vs majority 0.961
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+1.74; intercept=+1.92; fit acc 0.961 vs majority 0.961

### Agreement, all items, foil outcome = yes_correct (n=1228)

- pointing = both actants, role prompt: pointing hit 692/1228 (56.4%); kappa(foil, pointing) = 0.067; cells {'foil+point+': 634, 'foil+point-': 458, 'foil-point+': 58, 'foil-point-': 78}
- pointing = agent only, role prompt: pointing hit 0/1228 (0.0%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 0, 'foil+point-': 1092, 'foil-point+': 0, 'foil-point-': 136}
- pointing = both actants, noun prompt: pointing hit 1068/1228 (87.0%); kappa(foil, pointing) = 0.048; cells {'foil+point+': 956, 'foil+point-': 136, 'foil-point+': 112, 'foil-point-': 24}
- kappa(foil, blind) = 0.080; cells {'foil+point+': 955, 'foil+point-': 137, 'foil-point+': 107, 'foil-point-': 29}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.64, blind=+0.66; intercept=+1.21; fit acc 0.889 vs majority 0.889
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+0.60; intercept=+1.58; fit acc 0.889 vs majority 0.889

## aro-spatial (300 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 228/300 (76.0%) |
| pairwise, order-debiased | 219/300 (73.0%) |
| blind pairwise (no image) | 151/300 (50.3%) |
| mean P(yes) caption / foil | 0.186 / 0.070 |
| yes-rate (P(yes)>0.5) caption / foil | 0.090 / 0.003 |
| pairwise on the benchmark crop | 243/300 (81.0%) |

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| other-actant | noun_prompt | 484/600 (80.7%) | 484/600 (80.7%) | 0.807 | 600 |
| other-actant | role_prompt | 164/600 (27.3%) | 164/600 (27.3%) | 0.273 | 600 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 600, full_image_box 0.035, image_center_point 0.393, largest_role_box 0.500, other_actant_box 0.000, random_box 0.014
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): 
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 600, full_image_box 0.035, image_center_point 0.393, largest_role_box 0.500, other_actant_box 0.000, random_box 0.014

Both actants hit with role prompts, by role pair (top 8): object-subject 15/300

### Agreement, all items, foil outcome = pair_correct (n=300)

- pointing = both actants, role prompt: pointing hit 15/300 (5.0%); kappa(foil, pointing) = 0.019; cells {'foil+point+': 13, 'foil+point-': 206, 'foil-point+': 2, 'foil-point-': 79}
- pointing = agent only, role prompt: pointing hit 0/300 (0.0%); kappa(foil, pointing) = 0.000; cells {'foil+point+': 0, 'foil+point-': 219, 'foil-point+': 0, 'foil-point-': 81}
- pointing = both actants, noun prompt: pointing hit 194/300 (64.7%); kappa(foil, pointing) = 0.160; cells {'foil+point+': 152, 'foil+point-': 67, 'foil-point+': 42, 'foil-point-': 39}
- kappa(foil, blind) = 0.198; cells {'foil+point+': 125, 'foil+point-': 94, 'foil-point+': 26, 'foil-point-': 55}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.68, blind=+0.98; intercept=+0.53; fit acc 0.730 vs majority 0.730
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+0.96; intercept=+0.56; fit acc 0.730 vs majority 0.730

### Agreement, all items, foil outcome = yes_correct (n=300)

- pointing = both actants, role prompt: pointing hit 15/300 (5.0%); kappa(foil, pointing) = 0.005; cells {'foil+point+': 12, 'foil+point-': 216, 'foil-point+': 3, 'foil-point-': 69}
- pointing = agent only, role prompt: pointing hit 0/300 (0.0%); kappa(foil, pointing) = 0.000; cells {'foil+point+': 0, 'foil+point-': 228, 'foil-point+': 0, 'foil-point-': 72}
- pointing = both actants, noun prompt: pointing hit 194/300 (64.7%); kappa(foil, pointing) = 0.166; cells {'foil+point+': 158, 'foil+point-': 70, 'foil-point+': 36, 'foil-point-': 36}
- kappa(foil, blind) = 0.097; cells {'foil+point+': 122, 'foil+point-': 106, 'foil-point+': 29, 'foil-point-': 43}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.21, blind=+0.50; intercept=+0.91; fit acc 0.760 vs majority 0.760
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.00, blind=+0.50; intercept=+0.92; fit acc 0.760 vs majority 0.760

## controls, actant-swap (933 items, 1866 role targets)

- text-only role resolution correct: 1623/1866 (87.0%) (agent 807/895 (90.2%), other 816/971 (84.0%))
- pointing hit, role prompt: unconditioned 1286/1866 (68.9%) | caption-conditioned 1504/1866 (80.6%) | noun prompt 1682/1866 (90.1%)
- caption-conditioned by target: agent 751/895 (83.9%), other 753/971 (77.5%)
- both participants by role: unconditioned 461/933 (49.4%) | conditioned 610/933 (65.4%)
- text resolved correctly but unconditioned pointing failed: 483/1623 (29.8%) of text-correct targets
- conflict pointing (foil caption in prompt), non-nested targets n=1666: image-consistent 500/1666 (30.0%), text-following 236/1666 (14.2%), both 485/1666 (29.1%), neither 445/1666 (26.7%); nested pairs excluded: 200

## controls, aro-relation (1228 items, 2456 role targets)

- text-only role resolution correct: 2133/2456 (86.8%) (agent n/a, other 2133/2456 (86.8%))
- pointing hit, role prompt: unconditioned 1802/2456 (73.4%) | caption-conditioned 2222/2456 (90.5%) | noun prompt 2286/2456 (93.1%)
- caption-conditioned by target: agent n/a, other 2222/2456 (90.5%)
- both participants by role: unconditioned 690/1228 (56.2%) | conditioned 1018/1228 (82.9%)
- text resolved correctly but unconditioned pointing failed: 576/2133 (27.0%) of text-correct targets
- conflict pointing (foil caption in prompt), non-nested targets n=1960: image-consistent 408/1960 (20.8%), text-following 339/1960 (17.3%), both 1096/1960 (55.9%), neither 117/1960 (6.0%); nested pairs excluded: 496

## blind likelihood baseline, actant-swap (933 items)

- caption more likely than foil (text only): 87.0% | clearly text-solvable (margin > 1.0 nat): 83.4% | balanced: 7.4% | foil preferred: 9.2%
- stratum solvable (n=778): foil pass 91.8%, both-by-role 50.3%, P(point | foil pass) 52.4%, cells {'foil+point+': 374, 'foil+point-': 340, 'foil-point+': 17, 'foil-point-': 47}
- stratum balanced (n=69): foil pass 89.9%, both-by-role 39.1%, P(point | foil pass) 43.5%, cells {'foil+point+': 27, 'foil+point-': 35, 'foil-point+': 0, 'foil-point-': 7}
- stratum foil_preferred (n=86): foil pass 84.9%, both-by-role 50.0%, P(point | foil pass) 52.1%, cells {'foil+point+': 38, 'foil+point-': 35, 'foil-point+': 5, 'foil-point-': 8}

## blind likelihood baseline, action-replacement (630 items)

- caption more likely than foil (text only): 67.8% | clearly text-solvable (margin > 1.0 nat): 61.6% | balanced: 11.3% | foil preferred: 27.1%

## blind likelihood baseline, aro-relation (1228 items)

- caption more likely than foil (text only): 95.2% | clearly text-solvable (margin > 1.0 nat): 92.4% | balanced: 5.0% | foil preferred: 2.6%
- stratum solvable (n=1132): foil pass 97.5%, both-by-role 57.9%, P(point | foil pass) 57.7%, cells {'foil+point+': 637, 'foil+point-': 467, 'foil-point+': 18, 'foil-point-': 10}
- stratum balanced (n=64): foil pass 81.2%, both-by-role 34.4%, P(point | foil pass) 42.3%, cells {'foil+point+': 22, 'foil+point-': 30, 'foil-point+': 0, 'foil-point-': 12}
- stratum foil_preferred (n=32): foil pass 75.0%, both-by-role 46.9%, P(point | foil pass) 50.0%, cells {'foil+point+': 12, 'foil+point-': 12, 'foil-point+': 3, 'foil-point-': 5}

## blind likelihood baseline, aro-spatial (300 items)

- caption more likely than foil (text only): 49.7% | clearly text-solvable (margin > 1.0 nat): 32.7% | balanced: 32.7% | foil preferred: 34.7%
- stratum solvable (n=98): foil pass 70.4%, both-by-role 6.1%, P(point | foil pass) 8.7%, cells {'foil+point+': 6, 'foil+point-': 63, 'foil-point+': 0, 'foil-point-': 29}
- stratum balanced (n=98): foil pass 76.5%, both-by-role 8.2%, P(point | foil pass) 8.0%, cells {'foil+point+': 6, 'foil+point-': 69, 'foil-point+': 2, 'foil-point-': 21}
- stratum foil_preferred (n=104): foil pass 72.1%, both-by-role 1.0%, P(point | foil pass) 1.3%, cells {'foil+point+': 1, 'foil+point-': 74, 'foil-point+': 0, 'foil-point-': 29}

