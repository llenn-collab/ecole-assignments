# Raw Chart Dump (verbatim field extract)

Source sha256 `083a393c855730e9bf62e792340b664ee922c1c6048ff1663a68f3030dcc70b7`. Immutable. Do not edit.

## Header

```json
{
  "system": {
    "school": "Yi Yun - Lun Zang Jia",
    "chart_type": "Hour Rotation Chart",
    "method": "Chai Bu Method"
  },
  "timing": {
    "solar_term": {
      "name": "White Dew",
      "yuan": "Middle",
      "day": 3
    },
    "four_pillars": {
      "year": "Bing-Wu",
      "month": "Ding-You",
      "day": "Bing-Xu",
      "hour": "Jia-Wu"
    },
    "voidness": {
      "day_void": [
        "Wu",
        "Wei"
      ],
      "hour_void": [
        "Chen",
        "Si"
      ]
    }
  },
  "element_prosperities": {
    "metal": "Prosperous",
    "water": "Strengthening",
    "earth": "Resting",
    "fire": "Imprisoned",
    "wood": "Dead"
  },
  "chart_config": {
    "structure": "Yin Dun 3",
    "lead_stem": "Jia-Wu Xin",
    "duty_star": "Tian Ying (Hero)",
    "duty_door": "Jing (Scenery)",
    "chart_pattern": "Fu Yin (All elements in home positions)"
  }
}
```

## Palace 1

```json
{
  "id": 1,
  "name": "Kan",
  "direction": "North",
  "element": "Water",
  "base_position": {
    "trigram_numbers": [
      6,
      1
    ],
    "hetu_numbers": [
      1,
      6
    ],
    "early_heaven_trigram": "Kun (8)",
    "home_god": "Zhi Fu (Chief)",
    "home_door": "Xiu (Rest)",
    "home_star": "Tian Peng (Grass)",
    "earthly_branches": [
      "Zi (Rat)"
    ]
  },
  "palace_stem_rules": {
    "stems_in_birth_stage": [
      "Xin"
    ]
  },
  "active_chart": {
    "stems": {
      "heaven": "Geng",
      "earth": "Geng",
      "hidden": "Geng"
    },
    "star": "Tian Peng (Grass)",
    "door": "Xiu (Rest)",
    "god": "Bai Hu (White Tiger)",
    "energy_state": {
      "door": "Strengthening",
      "star": {
        "seasonal": "Strengthening",
        "palace_relation": "Obsolete"
      },
      "palace": "Strengthening",
      "realm": "Outer"
    }
  }
}
```

## Palace 2

```json
{
  "id": 2,
  "name": "Kun",
  "direction": "Southwest",
  "element": "Earth",
  "base_position": {
    "trigram_numbers": [
      8,
      2
    ],
    "hetu_numbers": [
      5,
      10
    ],
    "early_heaven_trigram": "Xun (5)",
    "home_god": [
      "Zhu Que (Vermilion Bird)",
      "Xuan Wu (Black Tortoise)"
    ],
    "home_door": "Si (Death)",
    "home_star": "Tian Rui (Grain)",
    "earthly_branches": [
      "Wei (Goat)",
      "Shen (Monkey)"
    ]
  },
  "palace_stem_rules": {
    "stems_in_tomb": [
      "Jia",
      "Gui"
    ],
    "stems_in_clash_punishment": [
      "Ji"
    ],
    "stems_in_harm": [
      "Wu"
    ],
    "stems_in_birth_stage": [
      "Ren"
    ]
  },
  "active_chart": {
    "status": {
      "is_void": true,
      "has_horse_star": true
    },
    "stems": {
      "heaven": "Ji",
      "earth": "Ji",
      "hidden": "Ji",
      "center_guest": "Bing",
      "afflictions": [
        "Clash Punishment (Ji Xing)",
        "Self Punishment"
      ]
    },
    "star": [
      "Tian Rui (Grain)",
      "Tian Qin (Bird)"
    ],
    "door": "Si (Death)",
    "god": "Jiu Tian (Nine Heavens)",
    "energy_state": {
      "door": "Resting",
      "star": {
        "seasonal": "Strengthening",
        "palace_relation": "Prosperous"
      },
      "palace": "Resting",
      "realm": "Inner"
    }
  }
}
```

## Palace 3

```json
{
  "id": 3,
  "name": "Zhen",
  "direction": "East",
  "element": "Wood",
  "base_position": {
    "trigram_numbers": [
      4,
      3
    ],
    "hetu_numbers": [
      3,
      8
    ],
    "early_heaven_trigram": "Li (3)",
    "home_god": "Tai Yin (Moon)",
    "home_door": "Shang (Harm)",
    "home_star": "Tian Chong (Impulse)",
    "earthly_branches": [
      "Mao (Rabbit)"
    ]
  },
  "palace_stem_rules": {
    "stems_in_clash_punishment": [
      "Wu"
    ],
    "stems_in_harm": [
      "Ren"
    ],
    "stems_in_birth_stage": [
      "Gui"
    ]
  },
  "active_chart": {
    "stems": {
      "heaven": "Wu",
      "earth": "Wu",
      "hidden": "Wu",
      "afflictions": [
        "Six Instruments Clash Punishment (Liu Yi Ji Xing)"
      ]
    },
    "star": "Tian Chong (Impulse)",
    "door": "Shang (Harm)",
    "god": "Tai Yin (Moon)",
    "energy_state": {
      "door": "Dead",
      "star": {
        "seasonal": "Strengthening",
        "palace_relation": "Imprisoned"
      },
      "palace": "Dead",
      "realm": "Outer"
    }
  }
}
```

## Palace 4

```json
{
  "id": 4,
  "name": "Xun",
  "direction": "Southeast",
  "element": "Wood",
  "base_position": {
    "trigram_numbers": [
      5,
      4
    ],
    "hetu_numbers": [
      3,
      8
    ],
    "early_heaven_trigram": "Dui (2)",
    "home_god": "Liu He (Six Harmony)",
    "home_door": "Du (Restraint)",
    "home_star": "Tian Fu (Assistant)",
    "earthly_branches": [
      "Chen (Dragon)",
      "Si (Snake)"
    ]
  },
  "palace_stem_rules": {
    "stems_in_tomb": [
      "Xin",
      "Ren"
    ],
    "stems_in_clash_punishment": [
      "Ren",
      "Gui"
    ],
    "stems_in_harm": [
      "Gui"
    ],
    "stems_in_birth_stage": [
      "Geng"
    ]
  },
  "active_chart": {
    "status": {
      "is_void": true
    },
    "stems": {
      "heaven": "Yi",
      "earth": "Yi",
      "hidden": "Yi"
    },
    "star": "Tian Fu (Assistant)",
    "door": "Du (Restraint)",
    "god": "Teng She (Serpent)",
    "energy_state": {
      "door": "Dead",
      "star": {
        "seasonal": "Strengthening",
        "palace_relation": "Imprisoned"
      },
      "palace": "Dead",
      "realm": "Outer"
    }
  }
}
```

## Palace 5

```json
{
  "id": 5,
  "name": "Zhong",
  "direction": "Center",
  "element": "Earth",
  "base_position": {
    "hetu_numbers": [
      5,
      10
    ],
    "home_star": "Tian Qin (Bird)"
  },
  "active_chart": {
    "note": "Attached to Palace 2",
    "stems": {
      "heaven": "Bing",
      "earth": "Bing",
      "hidden": "Bing"
    },
    "god": "Tai Chang (Grand Blessing)",
    "energy_state": {
      "palace": "Resting"
    }
  }
}
```

## Palace 6

```json
{
  "id": 6,
  "name": "Qian",
  "direction": "Northwest",
  "element": "Metal",
  "base_position": {
    "trigram_numbers": [
      1,
      6
    ],
    "hetu_numbers": [
      4,
      9
    ],
    "early_heaven_trigram": "Gen (7)",
    "home_god": "Jiu Tian (Nine Heavens)",
    "home_door": "Kai (Open)",
    "home_star": "Tian Xin (Heart)",
    "earthly_branches": [
      "Xu (Dog)",
      "Hai (Pig)"
    ]
  },
  "palace_stem_rules": {
    "stems_in_tomb": [
      "Yi",
      "Bing",
      "Wu"
    ],
    "stems_in_harm": [
      "Geng"
    ]
  },
  "active_chart": {
    "stems": {
      "heaven": "Ding",
      "earth": "Ding",
      "hidden": "Ding"
    },
    "star": "Tian Xin (Heart)",
    "door": "Kai (Open)",
    "god": "Xuan Wu (Black Tortoise)",
    "energy_state": {
      "door": "Prosperous",
      "star": {
        "seasonal": "Strengthening",
        "palace_relation": "Strengthening"
      },
      "palace": "Prosperous",
      "realm": "Inner"
    }
  }
}
```

## Palace 7

```json
{
  "id": 7,
  "name": "Dui",
  "direction": "West",
  "element": "Metal",
  "base_position": {
    "trigram_numbers": [
      2,
      7
    ],
    "hetu_numbers": [
      4,
      9
    ],
    "early_heaven_trigram": "Kan (6)",
    "home_god": "Jiu Di (Nine Earths)",
    "home_door": "Jing (Fear)",
    "home_star": "Tian Zhu (Pillar)",
    "earthly_branches": [
      "You (Rooster)"
    ]
  },
  "palace_stem_rules": {
    "stems_in_harm": [
      "Ji"
    ],
    "stems_in_birth_stage": [
      "Ding",
      "Ji"
    ]
  },
  "active_chart": {
    "stems": {
      "heaven": "Gui",
      "earth": "Gui",
      "hidden": "Gui",
      "afflictions": [
        "Heavenly Net Spread"
      ]
    },
    "star": "Tian Zhu (Pillar)",
    "door": "Jing (Fear)",
    "god": "Jiu Di (Nine Earths)",
    "energy_state": {
      "door": "Prosperous",
      "star": {
        "seasonal": "Strengthening",
        "palace_relation": "Strengthening"
      },
      "palace": "Prosperous",
      "realm": "Inner"
    }
  }
}
```

## Palace 8

```json
{
  "id": 8,
  "name": "Gen",
  "direction": "Northeast",
  "element": "Earth",
  "base_position": {
    "trigram_numbers": [
      7,
      8
    ],
    "hetu_numbers": [
      5,
      10
    ],
    "early_heaven_trigram": "Zhen (4)",
    "home_god": "Teng She (Serpent)",
    "home_door": "Sheng (Life)",
    "home_star": "Tian Ren (Ambassador)",
    "earthly_branches": [
      "Chou (Ox)",
      "Yin (Tiger)"
    ]
  },
  "palace_stem_rules": {
    "stems_in_tomb": [
      "Ding",
      "Ji",
      "Geng"
    ],
    "stems_in_clash_punishment": [
      "Geng"
    ],
    "stems_in_harm": [
      "Xin"
    ],
    "stems_in_birth_stage": [
      "Bing",
      "Wu"
    ]
  },
  "active_chart": {
    "stems": {
      "heaven": "Ren",
      "earth": "Ren",
      "hidden": "Ren"
    },
    "star": "Tian Ren (Ambassador)",
    "door": "Sheng (Life)",
    "god": "Liu He (Six Harmony)",
    "energy_state": {
      "door": "Resting",
      "star": {
        "seasonal": "Strengthening",
        "palace_relation": "Prosperous"
      },
      "palace": "Resting",
      "realm": "Outer"
    }
  }
}
```

## Palace 9

```json
{
  "id": 9,
  "name": "Li",
  "direction": "South",
  "element": "Fire",
  "base_position": {
    "trigram_numbers": [
      3,
      9
    ],
    "hetu_numbers": [
      2,
      7
    ],
    "early_heaven_trigram": "Qian (1)",
    "home_god": [
      "Gou Chen (Hooked Array)",
      "Bai Hu (White Tiger)"
    ],
    "home_door": "Jing (Scenery)",
    "home_star": "Tian Ying (Hero)",
    "earthly_branches": [
      "Wu (Horse)"
    ]
  },
  "palace_stem_rules": {
    "stems_in_clash_punishment": [
      "Xin"
    ],
    "stems_in_birth_stage": [
      "Yi"
    ]
  },
  "active_chart": {
    "status": {
      "is_void": true,
      "is_duty_palace": true
    },
    "stems": {
      "heaven": "Xin",
      "earth": "Xin",
      "hidden": "Xin",
      "afflictions": [
        "Clash Punishment (Ji Xing)",
        "Self Punishment",
        "Fu Yin"
      ]
    },
    "star": "Tian Ying (Hero)",
    "door": "Jing (Scenery)",
    "god": "Zhi Fu (Chief)",
    "energy_state": {
      "door": "Imprisoned",
      "star": {
        "seasonal": "Strengthening",
        "palace_relation": "Resting"
      },
      "palace": "Imprisoned",
      "realm": "Inner"
    }
  }
}
```

