package com.gmail.heroes.heroes.service.enumeration;

import com.gmail.heroes.heroes.service.strategy.ThreatStrategy;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public enum EnumThreat implements ThreatStrategy {

    God{
        @Override
        public List<EnumHero> findHeroToDefend() {
            return Collections.singletonList(EnumHero.S);
        }
    },
    Dragon {
        @Override
        public List<EnumHero> findHeroToDefend() {
            return Arrays.asList(EnumHero.S,EnumHero.A);
        }
    },
    Tiger {
        @Override
        public List<EnumHero> findHeroToDefend() {
            return Arrays.asList(EnumHero.S,EnumHero.A,EnumHero.B);
        }
    },
    Wolf {
        @Override
        public List<EnumHero> findHeroToDefend() {
            return Arrays.asList(EnumHero.S,EnumHero.A,EnumHero.B,EnumHero.C);
        }
    }
}
