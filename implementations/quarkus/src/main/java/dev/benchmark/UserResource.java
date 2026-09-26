package dev.benchmark;

import jakarta.inject.Inject;
import jakarta.transaction.Transactional;
import jakarta.ws.rs.BeanParam;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.QueryParam;
import jakarta.ws.rs.core.MediaType;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Path("/")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class UserResource {

    @GET
    @Path("/hello")
    public Map<String, String> hello() {
        Map<String, String> response = new HashMap<>();
        response.put("message", "ok");
        response.put("stack", "quarkus");
        return response;
    }

    @GET
    @Path("/users")
    public List<User> listUsers(
            @QueryParam("page") int page,
            @QueryParam("size") int size) {
        if (size < 1) size = 20;
        if (size > 100) size = 100;
        if (page < 0) page = 0;
        return User.findActive(page, size);
    }

    @POST
    @Path("/users/search")
    @Transactional
    public List<User> searchUsers(@BeanParam SearchRequest request) {
        if (request.size < 1) request.size = 20;
        if (request.size > 100) request.size = 100;
        if (request.page < 0) request.page = 0;
        return User.search(request.name, request.city, request.page, request.size);
    }
}