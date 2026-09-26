package dev.benchmark;

import jakarta.ws.rs.QueryParam;
import jakarta.ws.rs.DefaultValue;

public class SearchRequest {

    public String name;
    public String city;

    @QueryParam("page")
    @DefaultValue("0")
    public int page = 0;

    @QueryParam("size")
    @DefaultValue("20")
    public int size = 20;
}