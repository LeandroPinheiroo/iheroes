package com.gmail.heroes.heroes.web.dto;


import com.gmail.heroes.heroes.service.enumeration.EnumHero;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class HeroDTO {

    private Long id;
    private String name;
    private EnumHero enumHero;
    private LocationDTO location;

}
