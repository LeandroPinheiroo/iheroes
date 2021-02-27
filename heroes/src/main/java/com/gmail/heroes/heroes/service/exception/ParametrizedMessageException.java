package com.gmail.heroes.heroes.service.exception;

public class ParametrizedMessageException extends RuntimeException{

    public ParametrizedMessageException(String errorMessage) {
        super(errorMessage);
    }
}
