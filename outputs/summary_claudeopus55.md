# Summary for claudeopus55

Gold check available: 409 of 933 checked actant-swap items have both actant boxes confirmed by Grounding DINO.

## actant-swap (200 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 129/200 (64.5%) |
| pairwise, order-debiased | 197/200 (98.5%) |
| blind pairwise (no image) | 174/200 (87.0%) |
| mean P(yes) caption / foil | 0.670 / 0.050 |
| yes-rate (P(yes)>0.5) caption / foil | 0.670 / 0.050 |

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| agent | noun_prompt | 169/194 (87.1%) | 191/194 (98.5%) | 0.815 | 0 |
| agent | role_prompt | 156/194 (80.4%) | 185/194 (95.4%) | 0.768 | 1 |
| other-actant | noun_prompt | 151/206 (73.3%) | 196/206 (95.1%) | 0.703 | 1 |
| other-actant | role_prompt | 141/206 (68.4%) | 189/206 (91.7%) | 0.651 | 1 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 400, full_image_box 0.335, image_center_point 0.693, largest_role_box 0.550, other_actant_box 0.100, random_box 0.017
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): n_targets 194, full_image_box 0.320, image_center_point 0.763, largest_role_box 0.562, other_actant_box 0.098, random_box 0.024
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 206, full_image_box 0.350, image_center_point 0.626, largest_role_box 0.539, other_actant_box 0.102, random_box 0.020

Both actants hit with role prompts, by role pair (top 8): agent-item 28/49; agent-vehicle 4/15; agent-target 7/12; agent-tool 6/10; agent-victim 8/9; agent-student 4/9; agent-destination 1/9; agent-contact 7/7

### Agreement, all items, foil outcome = pair_correct (n=200)

- pointing = both actants, role prompt: pointing hit 109/200 (54.5%); kappa(foil, pointing) = 0.014; cells {'foil+point+': 108, 'foil+point-': 89, 'foil-point+': 1, 'foil-point-': 2}
- pointing = agent only, role prompt: pointing hit 156/200 (78.0%); kappa(foil, pointing) = 0.059; cells {'foil+point+': 155, 'foil+point-': 42, 'foil-point+': 1, 'foil-point-': 2}
- pointing = both actants, noun prompt: pointing hit 127/200 (63.5%); kappa(foil, pointing) = -0.003; cells {'foil+point+': 125, 'foil+point-': 72, 'foil-point+': 2, 'foil-point-': 1}
- kappa(foil, blind) = 0.043; cells {'foil+point+': 172, 'foil+point-': 25, 'foil-point+': 2, 'foil-point-': 1}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.37, blind=+0.45; intercept=+3.61; fit acc 0.985 vs majority 0.985
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.81, blind=+0.43; intercept=+3.25; fit acc 0.985 vs majority 0.985

### Agreement, detector-verified gold only, foil outcome = pair_correct (n=88)

- pointing = both actants, role prompt: pointing hit 64/88 (72.7%); kappa(foil, pointing) = 0.000; cells {'foil+point+': 64, 'foil+point-': 24, 'foil-point+': 0, 'foil-point-': 0}
- pointing = agent only, role prompt: pointing hit 80/88 (90.9%); kappa(foil, pointing) = 0.000; cells {'foil+point+': 80, 'foil+point-': 8, 'foil-point+': 0, 'foil-point-': 0}
- pointing = both actants, noun prompt: pointing hit 80/88 (90.9%); kappa(foil, pointing) = 0.000; cells {'foil+point+': 80, 'foil+point-': 8, 'foil-point+': 0, 'foil-point-': 0}
- kappa(foil, blind) = 0.000; cells {'foil+point+': 80, 'foil+point-': 8, 'foil-point+': 0, 'foil-point-': 0}
- logistic: foil_correct ~ pointing(both,role) + blind: degenerate outcome
- logistic: foil_correct ~ pointing(agent,role) + blind: degenerate outcome

### Agreement, all items, foil outcome = yes_correct (n=200)

- pointing = both actants, role prompt: pointing hit 109/200 (54.5%); kappa(foil, pointing) = 0.240; cells {'foil+point+': 82, 'foil+point-': 47, 'foil-point+': 27, 'foil-point-': 44}
- pointing = agent only, role prompt: pointing hit 156/200 (78.0%); kappa(foil, pointing) = 0.152; cells {'foil+point+': 107, 'foil+point-': 22, 'foil-point+': 49, 'foil-point-': 22}
- pointing = both actants, noun prompt: pointing hit 127/200 (63.5%); kappa(foil, pointing) = 0.154; cells {'foil+point+': 89, 'foil+point-': 40, 'foil-point+': 38, 'foil-point-': 33}
- kappa(foil, blind) = -0.006; cells {'foil+point+': 112, 'foil+point-': 17, 'foil-point+': 62, 'foil-point-': 9}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.96, blind=+0.03; intercept=+0.08; fit acc 0.645 vs majority 0.645
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.70, blind=-0.08; intercept=+0.13; fit acc 0.645 vs majority 0.645

### Agreement, detector-verified gold only, foil outcome = yes_correct (n=88)

- pointing = both actants, role prompt: pointing hit 64/88 (72.7%); kappa(foil, pointing) = 0.256; cells {'foil+point+': 49, 'foil+point-': 12, 'foil-point+': 15, 'foil-point-': 12}
- pointing = agent only, role prompt: pointing hit 80/88 (90.9%); kappa(foil, pointing) = 0.169; cells {'foil+point+': 58, 'foil+point-': 3, 'foil-point+': 22, 'foil-point-': 5}
- pointing = both actants, noun prompt: pointing hit 80/88 (90.9%); kappa(foil, pointing) = 0.036; cells {'foil+point+': 56, 'foil+point-': 5, 'foil-point+': 24, 'foil-point-': 3}
- kappa(foil, blind) = 0.036; cells {'foil+point+': 56, 'foil+point-': 5, 'foil-point+': 24, 'foil-point-': 3}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.95, blind=+0.23; intercept=-0.05; fit acc 0.693 vs majority 0.693
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.94, blind=+0.19; intercept=-0.20; fit acc 0.716 vs majority 0.693

## controls, actant-swap (200 items, 400 role targets)

- text-only role resolution correct: 378/400 (94.5%) (agent 188/194 (96.9%), other 190/206 (92.2%))
- pointing hit, role prompt: unconditioned 297/400 (74.2%) | caption-conditioned 310/400 (77.5%) | noun prompt 320/400 (80.0%)
- caption-conditioned by target: agent 164/194 (84.5%), other 146/206 (70.9%)
- both participants by role: unconditioned 109/200 (54.5%) | conditioned 118/200 (59.0%)
- text resolved correctly but unconditioned pointing failed: 96/378 (25.4%) of text-correct targets
- conflict pointing (foil caption in prompt), non-nested targets n=360: image-consistent 219/360 (60.8%), text-following 79/360 (21.9%), both 5/360 (1.4%), neither 57/360 (15.8%); nested pairs excluded: 40

