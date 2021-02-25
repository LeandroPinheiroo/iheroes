package com.gmail.heroes.heroes.service;

import com.gmail.heroes.heroes.domain.Hero;
import com.gmail.heroes.heroes.repository.HeroRepository;
import com.gmail.heroes.heroes.service.exception.ParametrizedMessageException;
import com.gmail.heroes.heroes.service.mapper.HeroMapper;
import com.gmail.heroes.heroes.web.dto.HeroDTO;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import javax.transaction.Transactional;

@Service
@RequiredArgsConstructor
@Transactional
@Slf4j
public class HeroService {

    private final HeroRepository heroRepository;
    private final HeroMapper heroMapper;

    public HeroDTO save(HeroDTO heroDTO){
        return this.heroMapper.toDto(this.heroRepository.save(this.heroMapper.toEntity(heroDTO)));
    }

    public Page<HeroDTO> findAll(Pageable pageable) {
        return heroRepository.findAll(pageable).map(heroMapper::toDto);
    }

    public HeroDTO findById(Long id) {
        return heroMapper.toDto(heroRepository.findById(id).orElse(new Hero()));
    }

    public HeroDTO delete(Long id) throws ParametrizedMessageException {
        Hero hero = heroRepository.findById(id).orElseThrow(() -> new ParametrizedMessageException("Herói não encontrado"));
        heroRepository.delete(hero);
        return this.heroMapper.toDto(hero);
    }

}
