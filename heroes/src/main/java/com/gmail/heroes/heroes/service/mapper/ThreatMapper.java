package com.gmail.heroes.heroes.service.mapper;


import com.gmail.heroes.heroes.domain.Threat;
import com.gmail.heroes.heroes.web.dto.ThreatDTO;
import org.mapstruct.Mapper;
import org.springframework.stereotype.Component;

@Component
@Mapper(componentModel = "spring", uses = {LocationMapper.class})
public interface ThreatMapper {

    ThreatDTO toDto(Threat user);

    Threat toEntity(ThreatDTO userDTO);



}
