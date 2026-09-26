package dev.benchmark;

import io.quarkus.hibernate.orm.panache.PanacheEntityBase;
import io.quarkus.panache.common.Page;
import io.quarkus.panache.common.Sort;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.OffsetDateTime;
import java.util.List;
import java.util.UUID;

@Entity
@Table(name = "users")
public class User extends PanacheEntityBase {

    @Id
    @Column(name = "id", nullable = false, updatable = false)
    public UUID id;

    @Column(name = "name", nullable = false, length = 100)
    public String name;

    @Column(name = "email", nullable = false, unique = true, length = 150)
    public String email;

    @Column(name = "city", nullable = false, length = 100)
    public String city;

    @Column(name = "country", nullable = false, length = 100)
    public String country;

    @Column(name = "age", nullable = false)
    public Integer age;

    @Column(name = "active", nullable = false)
    public Boolean active;

    @Column(name = "created_at", nullable = false)
    public OffsetDateTime createdAt;

    public static User findById(UUID id) {
        return find("id", id).firstResult();
    }

    public static List<User> findActive(int page, int size) {
        return find("active = true", Sort.by("createdAt").descending())
                .page(Page.of(page, size))
                .list();
    }

    public static List<User> search(String name, String city, int page, int size) {
        StringBuilder query = new StringBuilder("active = true");
        List<Object> params = new java.util.ArrayList<>();
        
        if (name != null && !name.isBlank()) {
            query.append(" AND name ILIKE ?");
            params.add("%" + name + "%");
        }
        if (city != null && !city.isBlank()) {
            query.append(" AND city ILIKE ?");
            params.add("%" + city + "%");
        }
        
        Object[] paramsArray = params.toArray();
        return find(query.toString(), Sort.by("createdAt").descending(), paramsArray)
                .page(Page.of(page, size))
                .list();
    }
}