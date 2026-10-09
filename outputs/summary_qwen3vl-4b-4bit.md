# Summary for qwen3vl-4b-4bit

Gold check available: 409 of 933 checked actant-swap items have both actant boxes confirmed by Grounding DINO.

## actant-swap (933 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 822/933 (88.1%) |
| pairwise, order-debiased | 892/933 (95.6%) |
| blind pairwise (no image) | 277/933 (29.7%) |
| mean P(yes) caption / foil | 0.450 / 0.033 |
| yes-rate (P(yes)>0.5) caption / foil | 0.445 / 0.029 |

Verb naming: strict 206/933 (22.1%), WordNet-synonym 241/933 (25.8%)

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| agent | noun_prompt | 735/895 (82.1%) | 854/895 (95.4%) | 0.798 | 13 |
| agent | role_prompt | 702/895 (78.4%) | 839/895 (93.7%) | 0.772 | 7 |
| other-actant | noun_prompt | 711/971 (73.2%) | 888/971 (91.5%) | 0.701 | 14 |
| other-actant | role_prompt | 578/971 (59.5%) | 811/971 (83.5%) | 0.590 | 39 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 1866, full_image_box 0.311, image_center_point 0.671, largest_role_box 0.554, other_actant_box 0.107, random_box 0.020
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): n_targets 895, full_image_box 0.352, image_center_point 0.769, largest_role_box 0.639, other_actant_box 0.107, random_box 0.026
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 971, full_image_box 0.273, image_center_point 0.582, largest_role_box 0.475, other_actant_box 0.107, random_box 0.018

Both actants hit with role prompts, by role pair (top 8): agent-item 110/202; agent-victim 42/66; agent-vehicle 16/54; agent-target 14/52; agent-tool 20/48; agent-destination 4/38; agent-student 13/37; agent-contact 22/31

### Agreement, all items, foil outcome = pair_correct (n=933)

- pointing = both actants, role prompt: pointing hit 429/933 (46.0%); kappa(foil, pointing) = 0.023; cells {'foil+point+': 416, 'foil+point-': 476, 'foil-point+': 13, 'foil-point-': 28}
- pointing = agent only, role prompt: pointing hit 702/933 (75.2%); kappa(foil, pointing) = 0.046; cells {'foil+point+': 677, 'foil+point-': 215, 'foil-point+': 25, 'foil-point-': 16}
- pointing = both actants, noun prompt: pointing hit 568/933 (60.9%); kappa(foil, pointing) = -0.000; cells {'foil+point+': 543, 'foil+point-': 349, 'foil-point+': 25, 'foil-point-': 16}
- kappa(foil, blind) = -0.015; cells {'foil+point+': 260, 'foil+point-': 632, 'foil-point+': 17, 'foil-point-': 24}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.57, blind=-0.49; intercept=+3.02; fit acc 0.956 vs majority 0.956
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.63, blind=-0.48; intercept=+2.81; fit acc 0.956 vs majority 0.956

### Agreement, detector-verified gold only, foil outcome = pair_correct (n=409)

- pointing = both actants, role prompt: pointing hit 260/409 (63.6%); kappa(foil, pointing) = 0.068; cells {'foil+point+': 250, 'foil+point-': 135, 'foil-point+': 10, 'foil-point-': 14}
- pointing = agent only, role prompt: pointing hit 347/409 (84.8%); kappa(foil, pointing) = 0.085; cells {'foil+point+': 330, 'foil+point-': 55, 'foil-point+': 17, 'foil-point-': 7}
- pointing = both actants, noun prompt: pointing hit 361/409 (88.3%); kappa(foil, pointing) = 0.006; cells {'foil+point+': 340, 'foil+point-': 45, 'foil-point+': 21, 'foil-point-': 3}
- kappa(foil, blind) = -0.019; cells {'foil+point+': 116, 'foil+point-': 269, 'foil-point+': 10, 'foil-point-': 14}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.79, blind=-0.38; intercept=+2.48; fit acc 0.941 vs majority 0.941
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.70, blind=-0.38; intercept=+2.35; fit acc 0.941 vs majority 0.941

### Agreement, all items, foil outcome = yes_correct (n=933)

- pointing = both actants, role prompt: pointing hit 429/933 (46.0%); kappa(foil, pointing) = 0.069; cells {'foil+point+': 395, 'foil+point-': 427, 'foil-point+': 34, 'foil-point-': 77}
- pointing = agent only, role prompt: pointing hit 702/933 (75.2%); kappa(foil, pointing) = 0.094; cells {'foil+point+': 632, 'foil+point-': 190, 'foil-point+': 70, 'foil-point-': 41}
- pointing = both actants, noun prompt: pointing hit 568/933 (60.9%); kappa(foil, pointing) = 0.065; cells {'foil+point+': 513, 'foil+point-': 309, 'foil-point+': 55, 'foil-point-': 56}
- kappa(foil, blind) = -0.017; cells {'foil+point+': 239, 'foil+point-': 583, 'foil-point+': 38, 'foil-point-': 73}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.70, blind=-0.22; intercept=+1.79; fit acc 0.881 vs majority 0.881
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.63, blind=-0.21; intercept=+1.62; fit acc 0.881 vs majority 0.881

### Agreement, detector-verified gold only, foil outcome = yes_correct (n=409)

- pointing = both actants, role prompt: pointing hit 260/409 (63.6%); kappa(foil, pointing) = 0.080; cells {'foil+point+': 236, 'foil+point-': 125, 'foil-point+': 24, 'foil-point-': 24}
- pointing = agent only, role prompt: pointing hit 347/409 (84.8%); kappa(foil, pointing) = 0.099; cells {'foil+point+': 311, 'foil+point-': 50, 'foil-point+': 36, 'foil-point-': 12}
- pointing = both actants, noun prompt: pointing hit 361/409 (88.3%); kappa(foil, pointing) = 0.079; cells {'foil+point+': 322, 'foil+point-': 39, 'foil-point+': 39, 'foil-point-': 9}
- kappa(foil, blind) = -0.024; cells {'foil+point+': 108, 'foil+point-': 253, 'foil-point+': 18, 'foil-point-': 30}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.57, blind=-0.27; intercept=+1.78; fit acc 0.883 vs majority 0.883
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.62, blind=-0.27; intercept=+1.61; fit acc 0.883 vs majority 0.883

## action-replacement (630 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 590/630 (93.7%) |
| pairwise, order-debiased | 603/630 (95.7%) |
| blind pairwise (no image) | 242/630 (38.4%) |
| mean P(yes) caption / foil | 0.440 / 0.033 |

- agent pointing, role_prompt: IoU>=0.5 492/630 (78.1%), mean IoU 0.763
- agent pointing, noun_prompt: IoU>=0.5 505/630 (80.2%), mean IoU 0.771
- kappa(foil, agent pointing) = 0.027; cells {'foil+point+': 473, 'foil+point-': 130, 'foil-point+': 19, 'foil-point-': 8}
- kappa(foil, blind) = -0.009; cells {'foil+point+': 230, 'foil+point-': 373, 'foil-point+': 12, 'foil-point-': 15}
- logistic: foil_correct ~ pointing + blind: coef: pointing=+0.37, blind=-0.24; intercept=+2.93; fit acc 0.957 vs majority 0.957

## controls (933 actant-swap items, 1866 role targets)

- text-only role resolution correct: 1720/1866 (92.2%) (agent 849/895 (94.9%), other 871/971 (89.7%))
- pointing hit, role prompt: unconditioned 1280/1866 (68.6%) | caption-conditioned 1351/1866 (72.4%) | noun prompt 1446/1866 (77.5%)
- caption-conditioned by target: agent 729/895 (81.5%), other 622/971 (64.1%)
- both participants by role: unconditioned 429/933 (46.0%) | conditioned 484/933 (51.9%)
- text resolved correctly but unconditioned pointing failed: 522/1720 (30.3%) of text-correct targets
- conflict pointing (foil caption in prompt), non-nested targets n=1666: image-consistent 1031/1666 (61.9%), text-following 277/1666 (16.6%), both 17/1666 (1.0%), neither 341/1666 (20.5%); nested pairs excluded: 200

## blind likelihood baseline, actant-swap (933 items)

- caption more likely than foil (text only): 89.1% | clearly text-solvable (margin > 1.0 nat): 84.4% | balanced: 7.9% | foil preferred: 7.7%
- stratum solvable (n=787): foil pass 96.6%, both-by-role 46.4%, P(point | foil pass) 47.1%, cells {'foil+point+': 358, 'foil+point-': 402, 'foil-point+': 7, 'foil-point-': 20}
- stratum balanced (n=74): foil pass 87.8%, both-by-role 51.4%, P(point | foil pass) 52.3%, cells {'foil+point+': 34, 'foil+point-': 31, 'foil-point+': 4, 'foil-point-': 5}
- stratum foil_preferred (n=72): foil pass 93.1%, both-by-role 36.1%, P(point | foil pass) 35.8%, cells {'foil+point+': 24, 'foil+point-': 43, 'foil-point+': 2, 'foil-point-': 3}

## blind likelihood baseline, action-replacement (630 items)

- caption more likely than foil (text only): 69.4% | clearly text-solvable (margin > 1.0 nat): 62.9% | balanced: 13.2% | foil preferred: 24.0%

