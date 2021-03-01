package com.gmail.heroes.heroes.domain;


import lombok.Getter;
import lombok.Setter;

import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.OneToOne;
import javax.validation.constraints.NotNull;
import java.time.LocalDateTime;

@Entity
@Getter
@Setter
public class History {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotNull
    @Column
    private LocalDateTime battleDate;

    @OneToOne(cascade = CascadeType.MERGE)
    @JoinColumn(name = "hero_id", referencedColumnName = "id")
    private Hero hero;

    @OneToOne(cascade = CascadeType.MERGE)
    @JoinColumn(name = "threat_id", referencedColumnName = "id")
    private Threat threat;

}
