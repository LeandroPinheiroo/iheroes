package com.gmail.heroes.heroes.web.dto;


import com.gmail.heroes.heroes.service.enumeration.EnumHero;
import com.gmail.heroes.heroes.service.enumeration.EnumThreat;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class ThreatDTO {

    private Long id;
    private String name;
    private EnumThreat enumThreat;
    private EnumHero dangerLevel;
    private LocationDTO location;

}
