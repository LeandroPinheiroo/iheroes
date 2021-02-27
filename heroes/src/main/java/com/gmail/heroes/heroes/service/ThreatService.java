package com.gmail.heroes.heroes.service;

import com.gmail.heroes.heroes.domain.Threat;
import com.gmail.heroes.heroes.repository.ThreatRepository;
import com.gmail.heroes.heroes.service.mapper.ThreatMapper;
import com.gmail.heroes.heroes.web.dto.ThreatDTO;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import javax.transaction.Transactional;

@Service
@RequiredArgsConstructor
@Transactional
@Slf4j
public class ThreatService {

    private final ThreatRepository threatRepository;
    private final ThreatMapper threatMapper;

    public ThreatDTO save(ThreatDTO threatDTO){
        Threat threat = threatRepository.findByName(threatDTO.getName()).orElse(threatMapper.toEntity(threatDTO));
        return this.threatMapper.toDto(this.threatRepository.save(threat));
    }
}
