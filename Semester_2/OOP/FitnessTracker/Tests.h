#ifndef TESTS_H
#define TESTS_H

#include "JSONRepository.h"
#include "Controller.h"
#include "ActivityFilter.h"
#include <cassert>
#include <cstdio>
#include <filesystem>

inline void runAllTests() {
    std::filesystem::remove("test_data.json");
    std::filesystem::remove("test_data2.json");
    std::filesystem::remove("test_data3.json");

    {
        JSONRepository repo("test_data.json");
        User u("u1", "TestUser");
        repo.addUser(u);
        assert(repo.getAllUsers().size() == 1);
        assert(repo.getUserById("u1").getName() == "TestUser");
    }

    {
        auto repo = std::make_unique<JSONRepository>("test_data2.json");
        Controller ctrl(std::move(repo));
        ctrl.addUser("u2", "User2");
        ctrl.setCurrentUser("u2");

        ctrl.addActivityToCurrentUser("a1", "Running", 40, 400, "2026-01-01");
        assert(ctrl.getCurrentUserActivities().size() == 1);

        ctrl.undo();
        assert(ctrl.getCurrentUserActivities().empty());

        ctrl.redo();
        assert(ctrl.getCurrentUserActivities().size() == 1);
    }

    {
        auto repo = std::make_unique<JSONRepository>("test_data3.json");
        Controller ctrl(std::move(repo));
        ctrl.addUser("u3", "User3");
        ctrl.setCurrentUser("u3");

        ctrl.addActivityToCurrentUser("a1", "Running", 50, 500, "2026-01-01");
        ctrl.addActivityToCurrentUser("a2", "Cycling", 20, 200, "2026-01-02");

        TypeSpecification typeSpec("Running");
        DurationSpecification durSpec(30);

        AndSpecification andSpec(std::make_shared<TypeSpecification>("Running"), std::make_shared<DurationSpecification>(30));
        auto resAnd = ctrl.getFilteredActivities(andSpec);
        assert(resAnd.size() == 1);

        OrSpecification orSpec(std::make_shared<TypeSpecification>("Running"), std::make_shared<DurationSpecification>(10));
        auto resOr = ctrl.getFilteredActivities(orSpec);
        assert(resOr.size() == 2);
    }

    std::filesystem::remove("test_data.json");
    std::filesystem::remove("test_data2.json");
    std::filesystem::remove("test_data3.json");

    std::printf("ALL TESTS PASSED SUCCESSFULLY!\n");
}

#endif // TESTS_H
