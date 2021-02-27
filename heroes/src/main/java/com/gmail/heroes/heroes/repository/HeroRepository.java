package com.gmail.heroes.heroes.repository;

import com.gmail.heroes.heroes.domain.Hero;
import com.gmail.heroes.heroes.service.enumeration.EnumHero;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface HeroRepository extends JpaRepository<Hero, Long> {

    List<Hero> findHeroByEnumHero(EnumHero enumHero);

}
