# Summary for gemini31pro

Gold check available: 409 of 933 checked actant-swap items have both actant boxes confirmed by Grounding DINO.

## actant-swap (200 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | 133/200 (66.5%) |
| pairwise, order-debiased | 181/200 (90.5%) |
| blind pairwise (no image) | 176/200 (88.0%) |
| mean P(yes) caption / foil | 0.695 / 0.058 |
| yes-rate (P(yes)>0.5) caption / foil | 0.680 / 0.050 |

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| agent | noun_prompt | 162/194 (83.5%) | 185/194 (95.4%) | 0.807 | 0 |
| agent | role_prompt | 166/194 (85.6%) | 187/194 (96.4%) | 0.813 | 0 |
| other-actant | noun_prompt | 144/206 (69.9%) | 193/206 (93.7%) | 0.682 | 1 |
| other-actant | role_prompt | 133/206 (64.6%) | 187/206 (90.8%) | 0.636 | 0 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 400, full_image_box 0.335, image_center_point 0.693, largest_role_box 0.550, other_actant_box 0.100, random_box 0.019
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): n_targets 194, full_image_box 0.320, image_center_point 0.763, largest_role_box 0.562, other_actant_box 0.098, random_box 0.022
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 206, full_image_box 0.350, image_center_point 0.626, largest_role_box 0.539, other_actant_box 0.102, random_box 0.019

Both actants hit with role prompts, by role pair (top 8): agent-item 33/49; agent-vehicle 5/15; agent-target 7/12; agent-tool 7/10; agent-victim 8/9; agent-student 4/9; agent-destination 1/9; agent-contact 7/7

### Agreement, all items, foil outcome = pair_correct (n=200)

- pointing = both actants, role prompt: pointing hit 113/200 (56.5%); kappa(foil, pointing) = 0.039; cells {'foil+point+': 104, 'foil+point-': 77, 'foil-point+': 9, 'foil-point-': 10}
- pointing = agent only, role prompt: pointing hit 166/200 (83.0%); kappa(foil, pointing) = 0.033; cells {'foil+point+': 151, 'foil+point-': 30, 'foil-point+': 15, 'foil-point-': 4}
- pointing = both actants, noun prompt: pointing hit 122/200 (61.0%); kappa(foil, pointing) = 0.063; cells {'foil+point+': 113, 'foil+point-': 68, 'foil-point+': 9, 'foil-point-': 10}
- kappa(foil, blind) = 0.246; cells {'foil+point+': 164, 'foil+point-': 17, 'foil-point+': 12, 'foil-point-': 7}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.35, blind=+1.34; intercept=+0.98; fit acc 0.905 vs majority 0.905
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.23, blind=+1.33; intercept=+0.99; fit acc 0.905 vs majority 0.905

### Agreement, detector-verified gold only, foil outcome = pair_correct (n=88)

- pointing = both actants, role prompt: pointing hit 67/88 (76.1%); kappa(foil, pointing) = -0.083; cells {'foil+point+': 63, 'foil+point-': 21, 'foil-point+': 4, 'foil-point-': 0}
- pointing = agent only, role prompt: pointing hit 86/88 (97.7%); kappa(foil, pointing) = -0.031; cells {'foil+point+': 82, 'foil+point-': 2, 'foil-point+': 4, 'foil-point-': 0}
- pointing = both actants, noun prompt: pointing hit 76/88 (86.4%); kappa(foil, pointing) = 0.061; cells {'foil+point+': 73, 'foil+point-': 11, 'foil-point+': 3, 'foil-point-': 1}
- kappa(foil, blind) = 0.097; cells {'foil+point+': 76, 'foil+point-': 8, 'foil-point+': 3, 'foil-point-': 1}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=-0.59, blind=+0.40; intercept=+3.17; fit acc 0.955 vs majority 0.955
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=-0.08, blind=+0.41; intercept=+2.76; fit acc 0.955 vs majority 0.955

### Agreement, all items, foil outcome = yes_correct (n=200)

- pointing = both actants, role prompt: pointing hit 113/200 (56.5%); kappa(foil, pointing) = 0.081; cells {'foil+point+': 79, 'foil+point-': 54, 'foil-point+': 34, 'foil-point-': 33}
- pointing = agent only, role prompt: pointing hit 166/200 (83.0%); kappa(foil, pointing) = 0.092; cells {'foil+point+': 114, 'foil+point-': 19, 'foil-point+': 52, 'foil-point-': 15}
- pointing = both actants, noun prompt: pointing hit 122/200 (61.0%); kappa(foil, pointing) = 0.040; cells {'foil+point+': 83, 'foil+point-': 50, 'foil-point+': 39, 'foil-point-': 28}
- kappa(foil, blind) = 0.052; cells {'foil+point+': 119, 'foil+point-': 14, 'foil-point+': 57, 'foil-point-': 10}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.33, blind=+0.34; intercept=+0.21; fit acc 0.665 vs majority 0.665
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=+0.48, blind=+0.34; intercept=-0.00; fit acc 0.665 vs majority 0.665

### Agreement, detector-verified gold only, foil outcome = yes_correct (n=88)

- pointing = both actants, role prompt: pointing hit 67/88 (76.1%); kappa(foil, pointing) = 0.032; cells {'foil+point+': 44, 'foil+point-': 13, 'foil-point+': 23, 'foil-point-': 8}
- pointing = agent only, role prompt: pointing hit 86/88 (97.7%); kappa(foil, pointing) = -0.045; cells {'foil+point+': 55, 'foil+point-': 2, 'foil-point+': 31, 'foil-point-': 0}
- pointing = both actants, noun prompt: pointing hit 76/88 (86.4%); kappa(foil, pointing) = -0.071; cells {'foil+point+': 48, 'foil+point-': 9, 'foil-point+': 28, 'foil-point-': 3}
- kappa(foil, blind) = -0.070; cells {'foil+point+': 50, 'foil+point-': 7, 'foil-point+': 29, 'foil-point-': 2}
- logistic: foil_correct ~ pointing(both,role) + blind: coef: pointing=+0.11, blind=-0.42; intercept=+0.91; fit acc 0.648 vs majority 0.648
- logistic: foil_correct ~ pointing(agent,role) + blind: coef: pointing=-0.51, blind=-0.44; intercept=+1.50; fit acc 0.648 vs majority 0.648

## controls, actant-swap (200 items, 400 role targets)

- text-only role resolution correct: 375/400 (93.8%) (agent 186/194 (95.9%), other 189/206 (91.7%))
- pointing hit, role prompt: unconditioned 299/400 (74.8%) | caption-conditioned 311/400 (77.8%) | noun prompt 306/400 (76.5%)
- caption-conditioned by target: agent 167/194 (86.1%), other 144/206 (69.9%)
- both participants by role: unconditioned 113/200 (56.5%) | conditioned 122/200 (61.0%)
- text resolved correctly but unconditioned pointing failed: 93/375 (24.8%) of text-correct targets
- conflict pointing (foil caption in prompt), non-nested targets n=360: image-consistent 214/360 (59.4%), text-following 80/360 (22.2%), both 3/360 (0.8%), neither 63/360 (17.5%); nested pairs excluded: 40

