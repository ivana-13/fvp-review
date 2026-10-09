# Summary for florence2-large

Gold check available: 409 of 933 checked actant-swap items have both actant boxes confirmed by Grounding DINO.

## actant-swap (933 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | n/a |
| pairwise, order-debiased | n/a |
| blind pairwise (no image) | n/a |
| mean P(yes) caption / foil | nan / nan |
| yes-rate (P(yes)>0.5) caption / foil | nan / nan |

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| agent | noun_prompt | 767/895 (85.7%) | 862/895 (96.3%) | 0.824 | 0 |
| agent | role_prompt | 703/895 (78.5%) | 822/895 (91.8%) | 0.766 | 0 |
| other-actant | noun_prompt | 727/971 (74.9%) | 871/971 (89.7%) | 0.725 | 0 |
| other-actant | role_prompt | 444/971 (45.7%) | 686/971 (70.6%) | 0.493 | 0 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 1866, full_image_box 0.311, image_center_point 0.671, largest_role_box 0.554, other_actant_box 0.107, random_box 0.020
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): n_targets 895, full_image_box 0.352, image_center_point 0.769, largest_role_box 0.639, other_actant_box 0.107, random_box 0.026
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 971, full_image_box 0.273, image_center_point 0.582, largest_role_box 0.475, other_actant_box 0.107, random_box 0.018

Both actants hit with role prompts, by role pair (top 8): agent-item 70/202; agent-victim 23/66; agent-vehicle 14/54; agent-target 12/52; agent-tool 24/48; agent-destination 7/38; agent-student 12/37; agent-contact 2/31

## action-replacement (630 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | n/a |
| pairwise, order-debiased | n/a |
| blind pairwise (no image) | n/a |
| mean P(yes) caption / foil | nan / nan |

## aro-relation (1228 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | n/a |
| pairwise, order-debiased | n/a |
| blind pairwise (no image) | n/a |
| mean P(yes) caption / foil | nan / nan |
| yes-rate (P(yes)>0.5) caption / foil | nan / nan |

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| other-actant | noun_prompt | 2161/2456 (88.0%) | 2278/2456 (92.8%) | 0.836 | 0 |
| other-actant | role_prompt | 1267/2456 (51.6%) | 1831/2456 (74.6%) | 0.540 | 0 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 2456, full_image_box 0.281, image_center_point 0.634, largest_role_box 0.601, other_actant_box 0.202, random_box 0.021
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): 
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 2456, full_image_box 0.281, image_center_point 0.634, largest_role_box 0.601, other_actant_box 0.202, random_box 0.021

Both actants hit with role prompts, by role pair (top 8): object-subject 341/1228

## aro-spatial (300 items)

| foil probe | correct |
|---|---|
| P(yes) caption > P(yes) foil | n/a |
| pairwise, order-debiased | n/a |
| blind pairwise (no image) | n/a |
| mean P(yes) caption / foil | nan / nan |
| yes-rate (P(yes)>0.5) caption / foil | nan / nan |

| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |
|---|---|---|---|---|---|
| other-actant | noun_prompt | 403/600 (67.2%) | 450/600 (75.0%) | 0.666 | 0 |
| other-actant | role_prompt | 131/600 (21.8%) | 227/600 (37.8%) | 0.259 | 0 |

Chance baselines for pointing, targets=all (IoU>=0.5 hit rate unless noted): n_targets 600, full_image_box 0.035, image_center_point 0.393, largest_role_box 0.500, other_actant_box 0.000, random_box 0.014
Chance baselines for pointing, targets=agent (IoU>=0.5 hit rate unless noted): 
Chance baselines for pointing, targets=other (IoU>=0.5 hit rate unless noted): n_targets 600, full_image_box 0.035, image_center_point 0.393, largest_role_box 0.500, other_actant_box 0.000, random_box 0.014

Both actants hit with role prompts, by role pair (top 8): object-subject 11/300

