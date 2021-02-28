package com.gmail.heroes.heroes.service;

import com.gmail.heroes.heroes.domain.Hero;
import com.gmail.heroes.heroes.domain.Threat;
import com.gmail.heroes.heroes.repository.HeroRepository;
import com.gmail.heroes.heroes.service.exception.ParametrizedMessageException;
import com.gmail.heroes.heroes.service.mapper.HeroMapper;
import com.gmail.heroes.heroes.service.mapper.ThreatMapper;
import com.gmail.heroes.heroes.util.CoordinatesUtil;
import com.gmail.heroes.heroes.web.dto.HeroDTO;
import com.gmail.heroes.heroes.web.dto.HistoryDTO;
import com.gmail.heroes.heroes.web.dto.ThreatDTO;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import javax.transaction.Transactional;
import java.time.LocalDateTime;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Transactional
@Slf4j
public class HeroService {

    private final HeroRepository heroRepository;
    private final HeroMapper heroMapper;
    private final ThreatMapper threatMapper;
    private final ThreatService threatService;
    private final HistoryService historyService;

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
        threatDTO = threatService.save(threatDTO);
        double minDistance = Double.MAX_VALUE;
        for (Hero hero : heroRepository.findHeroByEnumHeroIn(threatDTO.getDangerLevel().findHeroToDefend())) {
            double distance = CoordinatesUtil.distance(hero.getLocation().getLat().doubleValue(),threatDTO.getLocation().getLat().doubleValue(),hero.getLocation().getLng().doubleValue(),threatDTO.getLocation().getLng().doubleValue());
            if(distance < minDistance){
                minDistance = distance;
                heroToDefend = hero;
            }
        }
        Hero hero = Optional.ofNullable(heroToDefend).orElseThrow((() -> new ParametrizedMessageException("Herói não encontrado")));
        HeroDTO heroDTO = heroMapper.toDto(hero);
        historyService.save(hero,threatMapper.toEntity(threatDTO));
        return heroDTO;
    }
}
