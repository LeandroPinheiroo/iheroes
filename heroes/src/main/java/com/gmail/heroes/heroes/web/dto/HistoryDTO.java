package com.gmail.heroes.heroes.web.dto;


import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Getter
@Setter
public class HistoryDTO {

    private Long id;
    private LocalDateTime battleDate;
    private HeroDTO hero;
    private ThreatDTO threat;

}
