package com.gmail.heroes.heroes.security;

import com.gmail.heroes.heroes.web.dto.UserDTO;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.test.context.support.WithSecurityContextFactory;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public class RunWithMockCustomUserSecurityContextFactory implements WithSecurityContextFactory<RunWithMockCustomUser> {

    @Override
    public SecurityContext createSecurityContext(RunWithMockCustomUser customUser) {
        SecurityContext context = SecurityContextHolder.createEmptyContext();
        String token = UUID.randomUUID().toString();
        Map<String, Object> attributes = new HashMap<>();
        attributes.put("email", customUser.email());
        attributes.put("name", customUser.name());
        UserDTO userDTO = new UserDTO();
        userDTO.setName(customUser.name());

        context.setAuthentication(new UsernamePasswordAuthenticationToken(userDTO, token, Collections.emptyList()));
        return context;
    }
}
