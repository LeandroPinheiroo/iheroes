package com.gmail.heroes.heroes.web.dto;


import lombok.Getter;
import lombok.Setter;

import java.math.BigDecimal;

@Getter
@Setter
public class LocationDTO {

    private Long id;
    private BigDecimal lat;
    private BigDecimal lng;

}
