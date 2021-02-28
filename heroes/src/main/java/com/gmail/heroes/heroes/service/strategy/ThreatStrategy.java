package com.gmail.heroes.heroes.service.strategy;

import com.gmail.heroes.heroes.service.enumeration.EnumHero;

import java.util.List;

public interface ThreatStrategy {

    List<EnumHero> findHeroToDefend();
}
