package com.gmail.heroes.heroes.web;


import com.gmail.heroes.heroes.service.HeroService;
import com.gmail.heroes.heroes.service.exception.ParametrizedMessageException;
import com.gmail.heroes.heroes.web.dto.HeroDTO;
import com.gmail.heroes.heroes.web.dto.ThreatDTO;
import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.validation.Valid;
import java.util.List;


@RestController
@RequestMapping("/api/hero")
@RequiredArgsConstructor
@Validated
public class HeroResource {

    private final HeroService heroService;
    private final Logger log = LoggerFactory.getLogger(HeroResource.class);

    /**
     * POST /api/hero: request to save a hero
     *
     * @return HeroDto object saved
     */
    @PostMapping
    public ResponseEntity<HeroDTO> save(@Valid @RequestBody HeroDTO heroDTO) {
        log.debug("Request to save a new hero, {}",heroDTO);
        return ResponseEntity.ok(heroService.save(heroDTO));
    }

    /**
     * Get /api/hero: request to get all heroes
     *
     * @return List<HeroDto> object find
     */
    @GetMapping
    public ResponseEntity<Page<HeroDTO>> filterAll(Pageable pageable) {
        log.debug("REST request to filter All Heroes ");
        return ResponseEntity.ok(heroService.filterAll(pageable));
    }

    /**
     * Get /api/hero: request to get all heroes
     *
     * @return List<HeroDto> object find
     */
    @GetMapping("/find-all")
    public ResponseEntity<List<HeroDTO>> findAll() {
        log.debug("REST request to find All Heroes ");
        return ResponseEntity.ok(heroService.findAll());
    }

    /**
     * Get /api/hero/{ID}: request to get a hero by ID
     *
     * @return HeroDto object find
     */
    @GetMapping("/{id}")
    public ResponseEntity<HeroDTO> findById(@PathVariable("id") Long id) {
        log.debug("REST request to find a hero by id {} ", id);
        return ResponseEntity.ok(heroService.findById(id));
    }

    /**
     * PUT /api/hero/: request to Update a Hero
     *
     * @return HeroDto object updated
     */
    @PutMapping
    public ResponseEntity<HeroDTO> update(@Valid @RequestBody HeroDTO heroDTO) {
        log.debug("REST request to update a hero {}",heroDTO);
        return ResponseEntity.ok(heroService.save(heroDTO));
    }


    /**
     * DELETE /api/hero/{id}: request to Delete a Hero by ID
     *
     * @return HeroDto object removed
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<HeroDTO> delete(@PathVariable("id") Long id) throws ParametrizedMessageException {
        log.debug("REST request to delete a hero by id {}",id);
        return ResponseEntity.ok(heroService.delete(id));
    }


    /**
     * POST /api/hero/defend: request to save a hero
     *
     * @return HeroDto object saved
     */
    @PostMapping("/defend")
    public ResponseEntity<HeroDTO> getHeroDefend(@Valid @RequestBody ThreatDTO threatDTO) {
        log.debug("Request to get a hero to defend the world of the threat, {}",threatDTO);
        return ResponseEntity.ok(heroService.getHeroDefend(threatDTO));
    }
}
