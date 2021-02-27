package com.gmail.heroes.heroes.repository;

import com.gmail.heroes.heroes.domain.Threat;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface ThreatRepository extends JpaRepository<Threat, Long> {

    Optional<Threat> findByName(String name);

}
