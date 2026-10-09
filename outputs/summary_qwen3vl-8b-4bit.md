# Summary for qwen3vl-8b-4bit

Gold check available: 409 of 933 checked actant-swap items have both actant boxes confirmed by Grounding DINO.

## actant-swap (933 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 830/933 (89.0%) |
| pairwise, order-debiased | 891/933 (95.5%) |
| blind pairwise (no image) | 52/933 (5.6%) |
| mean P(yes) caption / foil | 0.422 / 0.030 |
| yes-rate (P(yes)>0.5) caption / foil | 0.413 / 0.023 |

Verb naming: strict 247/933 (26.5%), WordNet-synonym 283/933 (30.3%)

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| agent | noun_prompt | 733/895 (81.9%) | 852/895 (95.2%) | 0.794 | 10 |
| agent | role_prompt | 690/895 (77.1%) | 823/895 (92.0%) | 0.755 | 24 |
| other-actant | noun_prompt | 705/971 (72.6%) | 896/971 (92.3%) | 0.702 | 18 |
| other-actant | role_prompt | 588/971 (60.6%) | 826/971 (85.1%) | 0.598 | 44 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 1866, full_image_box 0.311, image_center_point 0.671, largest_role_box 0.554, other_actant_box 0.107, random_box 0.020
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): n_targets 895, full_image_box 0.352, image_center_point 0.769, largest_role_box 0.639, other_actant_box 0.107, random_box 0.026
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 971, full_image_box 0.273, image_center_point 0.582, largest_role_box 0.475, other_actant_box 0.107, random_box 0.018

Both actants hit with role prompts, by role pair (top 8): agent-item 107/202; agent-victim 43/66; agent-vehicle 17/54; agent-target 20/52; agent-tool 19/48; agent-destination 5/38; agent-student 15/37; agent-contact 24/31

### Agreement, all items, foil outcome = pair_correct (n=933)

- pointing = both actants, role prompt: pointing hit 444/933 (47.6%); kappa(foil, pointing) = 0.020; cells {'foil+point+': 429, 'foil+point-': 462, 'foil-point+': 15, 'foil-point-': 27}
- pointing = agent only, role prompt: pointing hit 690/933 (74.0%); kappa(foil, pointing) = 0.038; cells {'foil+point+': 664, 'foil+point-': 227, 'foil-point+': 26, 'foil-point-': 16}
- pointing = both actants, noun prompt: pointing hit 563/933 (60.3%); kappa(foil, pointing) = 0.018; cells {'foil+point+': 541, 'foil+point-': 350, 'foil-point+': 22, 'foil-point-': 20}
- kappa(foil, blind) = -0.013; cells {'foil+point+': 44, 'foil+point-': 847, 'foil-point+': 8, 'foil-point-': 34}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.53, blind=-1.34; intercept=+2.96; fit acc 0.955 vs majority 0.955
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.55, blind=-1.29; intercept=+2.80; fit acc 0.955 vs majority 0.955

### Agreement, detector-verified gold only, foil outcome = pair_correct (n=409)

- pointing = both actants, role prompt: pointing hit 265/409 (64.8%); kappa(foil, pointing) = 0.027; cells {'foil+point+': 256, 'foil+point-': 136, 'foil-point+': 9, 'foil-point-': 8}
- pointing = agent only, role prompt: pointing hit 351/409 (85.8%); kappa(foil, pointing) = 0.017; cells {'foil+point+': 337, 'foil+point-': 55, 'foil-point+': 14, 'foil-point-': 3}
- pointing = both actants, noun prompt: pointing hit 357/409 (87.3%); kappa(foil, pointing) = -0.036; cells {'foil+point+': 341, 'foil+point-': 51, 'foil-point+': 16, 'foil-point-': 1}
- kappa(foil, blind) = -0.016; cells {'foil+point+': 20, 'foil+point-': 372, 'foil-point+': 4, 'foil-point-': 13}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.48, blind=-1.28; intercept=+2.98; fit acc 0.958 vs majority 0.958
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.21, blind=-1.24; intercept=+3.09; fit acc 0.958 vs majority 0.958

### Agreement, all items, foil outcome = yes_correct (n=933)

- pointing = both actants, role prompt: pointing hit 444/933 (47.6%); kappa(foil, pointing) = 0.046; cells {'foil+point+': 406, 'foil+point-': 424, 'foil-point+': 38, 'foil-point-': 65}
- pointing = agent only, role prompt: pointing hit 690/933 (74.0%); kappa(foil, pointing) = 0.035; cells {'foil+point+': 619, 'foil+point-': 211, 'foil-point+': 71, 'foil-point-': 32}
- pointing = both actants, noun prompt: pointing hit 563/933 (60.3%); kappa(foil, pointing) = 0.062; cells {'foil+point+': 513, 'foil+point-': 317, 'foil-point+': 50, 'foil-point-': 53}
- kappa(foil, blind) = -0.021; cells {'foil+point+': 38, 'foil+point-': 792, 'foil-point+': 14, 'foil-point-': 89}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.52, blind=-1.14; intercept=+1.95; fit acc 0.890 vs majority 0.890
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.29, blind=-1.08; intercept=+1.97; fit acc 0.890 vs majority 0.890

### Agreement, detector-verified gold only, foil outcome = yes_correct (n=409)

- pointing = both actants, role prompt: pointing hit 265/409 (64.8%); kappa(foil, pointing) = 0.086; cells {'foil+point+': 242, 'foil+point-': 121, 'foil-point+': 23, 'foil-point-': 23}
- pointing = agent only, role prompt: pointing hit 351/409 (85.8%); kappa(foil, pointing) = -0.012; cells {'foil+point+': 311, 'foil+point-': 52, 'foil-point+': 40, 'foil-point-': 6}
- pointing = both actants, noun prompt: pointing hit 357/409 (87.3%); kappa(foil, pointing) = 0.050; cells {'foil+point+': 319, 'foil+point-': 44, 'foil-point+': 38, 'foil-point-': 8}
- kappa(foil, blind) = -0.013; cells {'foil+point+': 19, 'foil+point-': 344, 'foil-point+': 5, 'foil-point-': 41}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.66, blind=-0.70; intercept=+1.73; fit acc 0.888 vs majority 0.888
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=-0.08, blind=-0.61; intercept=+2.18; fit acc 0.888 vs majority 0.888

## action-replacement (630 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 579/630 (91.9%) |
| pairwise, order-debiased | 600/630 (95.2%) |
| blind pairwise (no image) | 194/630 (30.8%) |
| mean P(yes) caption / foil | 0.426 / 0.028 |

- agent pointing, role_prompt: IoU>=0.5 493/630 (78.3%), mean IoU 0.762
- agent pointing, noun_prompt: IoU>=0.5 495/630 (78.6%), mean IoU 0.758
- kappa(foil, agent pointing) = 0.045; cells {'foil+point+': 473, 'foil+point-': 127, 'foil-point+': 20, 'foil-point-': 10}
- kappa(foil, blind) = -0.018; cells {'foil+point+': 181, 'foil+point-': 419, 'foil-point+': 13, 'foil-point-': 17}
- logistic: foil_correct ~ pointing + blind: coef: pointing=+0.52, blind=-0.48; intercept=+2.79; fit acc 0.952 vs majority 0.952

## controls (933 actant-swap items, 1866 role targets)

- text-only role resolution correct: 1710/1866 (91.6%) (agent 839/895 (93.7%), other 871/971 (89.7%))
- pointing hit, role prompt: unconditioned 1278/1866 (68.5%) | caption-conditioned 1381/1866 (74.0%) | noun prompt 1438/1866 (77.1%)
- caption-conditioned by target: agent 733/895 (81.9%), other 648/971 (66.7%)
- both participants by role: unconditioned 444/933 (47.6%) | conditioned 506/933 (54.2%)
- text resolved correctly but unconditioned pointing failed: 535/1710 (31.3%) of text-correct targets
- conflict pointing (foil caption in prompt), non-nested targets n=1666: image-consistent 1004/1666 (60.3%), text-following 285/1666 (17.1%), both 15/1666 (0.9%), neither 362/1666 (21.7%); nested pairs excluded: 200

## blind likelihood baseline, actant-swap (933 items)

- caption more likely than foil (text only): 90.4% | clearly text-solvable (margin > 1.0 nat): 86.3% | balanced: 6.6% | foil preferred: 7.1%
- stratum solvable (n=805): foil pass 97.0%, both-by-role 47.2%, P(point | foil pass) 47.6%, cells {'foil+point+': 372, 'foil+point-': 409, 'foil-point+': 8, 'foil-point-': 16}
- stratum balanced (n=62): foil pass 88.7%, both-by-role 51.6%, P(point | foil pass) 52.7%, cells {'foil+point+': 29, 'foil+point-': 26, 'foil-point+': 3, 'foil-point-': 4}
- stratum foil_preferred (n=66): foil pass 83.3%, both-by-role 48.5%, P(point | foil pass) 50.9%, cells {'foil+point+': 28, 'foil+point-': 27, 'foil-point+': 4, 'foil-point-': 7}

## blind likelihood baseline, action-replacement (630 items)

- caption more likely than foil (text only): 69.4% | clearly text-solvable (margin > 1.0 nat): 63.0% | balanced: 13.2% | foil preferred: 23.8%

