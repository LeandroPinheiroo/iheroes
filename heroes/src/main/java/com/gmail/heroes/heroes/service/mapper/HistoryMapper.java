package com.gmail.heroes.heroes.service.mapper;


import com.gmail.heroes.heroes.domain.History;
import com.gmail.heroes.heroes.web.dto.HistoryDTO;
import org.mapstruct.Mapper;
import org.springframework.stereotype.Component;

@Component
@Mapper(componentModel = "spring", uses = {HeroMapper.class, ThreatMapper.class})
public interface HistoryMapper {

    HistoryDTO toDto(History user);

    History toEntity(HistoryDTO userDTO);
}
