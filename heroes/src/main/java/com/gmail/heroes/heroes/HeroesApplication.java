package com.gmail.heroes.heroes;

import com.gmail.heroes.heroes.config.properties.HeroesApiProperty;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;

@SpringBootApplication
@EnableConfigurationProperties(HeroesApiProperty.class)
public class HeroesApplication {

    public static void main(String[] args) {
        SpringApplication.run(HeroesApplication.class, args);
    }

}
