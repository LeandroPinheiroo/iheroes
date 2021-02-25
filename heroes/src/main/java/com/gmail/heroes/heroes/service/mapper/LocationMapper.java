package com.gmail.heroes.heroes.service.mapper;


import com.gmail.heroes.heroes.domain.Location;
import com.gmail.heroes.heroes.web.dto.LocationDTO;
import org.mapstruct.Mapper;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
@Mapper(componentModel = "spring")
public interface LocationMapper {

    LocationDTO toDto(Location user);

    List<LocationDTO> toDto(List<Location> user);

    Location toEntity(LocationDTO userDTO);



}
