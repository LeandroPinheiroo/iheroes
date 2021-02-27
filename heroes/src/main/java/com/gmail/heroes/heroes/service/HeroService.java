package com.gmail.heroes.heroes.service;

import com.gmail.heroes.heroes.domain.Hero;
import com.gmail.heroes.heroes.repository.HeroRepository;
import com.gmail.heroes.heroes.service.exception.ParametrizedMessageException;
import com.gmail.heroes.heroes.service.mapper.HeroMapper;
import com.gmail.heroes.heroes.util.CoordinatesUtil;
import com.gmail.heroes.heroes.web.dto.HeroDTO;
import com.gmail.heroes.heroes.web.dto.ThreatDTO;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import javax.transaction.Transactional;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Transactional
@Slf4j
public class HeroService {

    private final HeroRepository heroRepository;
    private final HeroMapper heroMapper;
    private final ThreatService threatService;

    public HeroDTO save(HeroDTO heroDTO){
        return this.heroMapper.toDto(this.heroRepository.save(this.heroMapper.toEntity(heroDTO)));
    }

    public Page<HeroDTO> findAll(Pageable pageable) {
        return heroRepository.findAll(pageable).map(heroMapper::toDto);
    }

    public HeroDTO findById(Long id) {
        return heroMapper.toDto(heroRepository.findById(id).orElse(new Hero()));
    }

    public HeroDTO delete(Long id) {
        Hero hero = heroRepository.findById(id).orElseThrow(() -> new ParametrizedMessageException("Herói não encontrado"));
        heroRepository.delete(hero);
        return this.heroMapper.toDto(hero);
    }

    public HeroDTO getHeroDefend(ThreatDTO threatDTO){
        Hero heroToDefend = null;
        threatService.save(threatDTO);
        double minDistance = Double.MAX_VALUE;
        for (Hero hero : heroRepository.findHeroByEnumHero(threatDTO.getDangerLevel())) {
            double distance = CoordinatesUtil.distance(hero.getLocation().getLatitude().doubleValue(),threatDTO.getLocation().getLatitude().doubleValue(),hero.getLocation().getLongitude().doubleValue(),threatDTO.getLocation().getLongitude().doubleValue());
            if(distance < minDistance){
                minDistance = distance;
                heroToDefend = hero;
            }
        }
        return heroMapper.toDto(Optional.ofNullable(heroToDefend).orElseThrow((() -> new ParametrizedMessageException("Herói não encontrado"))));
    }

}
