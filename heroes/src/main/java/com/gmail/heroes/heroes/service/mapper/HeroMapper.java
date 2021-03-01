package com.gmail.heroes.heroes.service.mapper;


import com.gmail.heroes.heroes.domain.Hero;
import com.gmail.heroes.heroes.web.dto.HeroDTO;
import org.mapstruct.Mapper;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
@Mapper(componentModel = "spring", uses = {LocationMapper.class})
public interface HeroMapper {

    HeroDTO toDto(Hero hero);

    List<HeroDTO> toDtoList(List<Hero> hero);

    Hero toEntity(HeroDTO heroDTO);



}
