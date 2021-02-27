package com.gmail.heroes.heroes.service;

import com.gmail.heroes.heroes.repository.HistoryRepository;
import com.gmail.heroes.heroes.service.mapper.HistoryMapper;
import com.gmail.heroes.heroes.web.dto.HeroDTO;
import com.gmail.heroes.heroes.web.dto.HistoryDTO;
import com.gmail.heroes.heroes.web.dto.ThreatDTO;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import javax.transaction.Transactional;
import java.time.LocalDateTime;

@Service
@RequiredArgsConstructor
@Transactional
@Slf4j
public class HistoryService {

    private final HistoryRepository historyRepository;
    private final HistoryMapper historyMapper;

    public HistoryDTO save(HeroDTO heroDTO, ThreatDTO threatDTO){
        HistoryDTO historyDTO = new HistoryDTO();
        historyDTO.setHero(heroDTO);
        historyDTO.setThreat(threatDTO);
        historyDTO.setBattleDate(LocalDateTime.now());
        return this.historyMapper.toDto(this.historyRepository.save(this.historyMapper.toEntity(historyDTO)));
    }

    public Page<HistoryDTO> findAll(Pageable pageable) {
        return historyRepository.findAll(pageable).map(historyMapper::toDto);
    }

}
