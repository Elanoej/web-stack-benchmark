package dev.benchmark.user

import org.springframework.data.domain.Page
import org.springframework.data.domain.PageImpl
import org.springframework.data.domain.Pageable
import org.springframework.stereotype.Repository
import jakarta.persistence.EntityManager

@Repository
class UserRepositoryImpl(
    private val entityManager: EntityManager
) : UserRepositoryCustom {

    override fun search(name: String?, city: String?, pageable: Pageable): Page<User> {
        val conditions = mutableListOf<String>()

        if (name != null) conditions.add("name ILIKE CONCAT('%', :name, '%')")
        if (city != null) conditions.add("city ILIKE CONCAT('%', :city, '%')")

        val whereClause = if (conditions.isNotEmpty()) conditions.joinToString(" AND ", " AND ", "") else ""
        val sql = "SELECT * FROM users WHERE active = true$whereClause ORDER BY created_at DESC"
        val countSql = "SELECT count(*) FROM users WHERE active = true$whereClause"

        val countQuery = entityManager.createNativeQuery(countSql)
        if (name != null) countQuery.setParameter("name", name)
        if (city != null) countQuery.setParameter("city", city)
        val total = (countQuery.singleResult as Number).toLong()

        val dataQuery = entityManager.createNativeQuery(sql, User::class.java)
        if (name != null) dataQuery.setParameter("name", name)
        if (city != null) dataQuery.setParameter("city", city)
        dataQuery.firstResult = pageable.pageNumber * pageable.pageSize
        dataQuery.maxResults = pageable.pageSize

        @Suppress("UNCHECKED_CAST")
        val users = dataQuery.resultList as List<User>
        return PageImpl(users, pageable, total)
    }
}
