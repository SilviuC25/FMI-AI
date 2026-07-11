#ifndef ACTIVITYFILTER_H
#define ACTIVITYFILTER_H

#include "Activity.h"
#include <memory>
#include <vector>
#include <string>

class ActivitySpecification {
public:
    virtual ~ActivitySpecification() = default;
    virtual bool isSatisfiedBy(const std::shared_ptr<Activity>& activity) const = 0;
};

class TypeSpecification : public ActivitySpecification {
private:
    std::string type;
public:
    TypeSpecification(const std::string& type);
    bool isSatisfiedBy(const std::shared_ptr<Activity>& activity) const override;
};

class DurationSpecification : public ActivitySpecification {
private:
    int minDuration;
public:
    DurationSpecification(int minMin);
    bool isSatisfiedBy(const std::shared_ptr<Activity>& activity) const override;
};

class AndSpecification : public ActivitySpecification {
private:
    std::shared_ptr<ActivitySpecification> spec1;
    std::shared_ptr<ActivitySpecification> spec2;
public:
    AndSpecification(std::shared_ptr<ActivitySpecification> s1, std::shared_ptr<ActivitySpecification> s2);
    bool isSatisfiedBy(const std::shared_ptr<Activity>& activity) const override;
};

class OrSpecification : public ActivitySpecification {
private:
    std::shared_ptr<ActivitySpecification> spec1;
    std::shared_ptr<ActivitySpecification> spec2;
public:
    OrSpecification(std::shared_ptr<ActivitySpecification> s1, std::shared_ptr<ActivitySpecification> s2);
    bool isSatisfiedBy(const std::shared_ptr<Activity>& activity) const override;
};

#endif // ACTIVITYFILTER_H
