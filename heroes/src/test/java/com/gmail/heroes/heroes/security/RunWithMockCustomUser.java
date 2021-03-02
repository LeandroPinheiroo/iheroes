package com.gmail.heroes.heroes.security;

import org.springframework.security.test.context.support.WithSecurityContext;

import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;

@Retention(RetentionPolicy.RUNTIME)
@WithSecurityContext(factory = RunWithMockCustomUserSecurityContextFactory.class)
public @interface RunWithMockCustomUser {

    String name() default "admin";

    String email() default "25425196504";
}

