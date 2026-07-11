#include "ActivityFilter.h"

TypeSpecification::TypeSpecification(const std::string& type) : type(type) {}

bool TypeSpecification::isSatisfiedBy(const std::shared_ptr<Activity>& activity) const {
    return activity->getType() == type;
}

DurationSpecification::DurationSpecification(int minMin) : minDuration(minMin) {}

bool DurationSpecification::isSatisfiedBy(const std::shared_ptr<Activity>& activity) const {
    return activity->getDuration() >= minDuration;
}

AndSpecification::AndSpecification(std::shared_ptr<ActivitySpecification> s1, std::shared_ptr<ActivitySpecification> s2)
    : spec1(s1), spec2(s2) {}

bool AndSpecification::isSatisfiedBy(const std::shared_ptr<Activity>& activity) const {
    return spec1->isSatisfiedBy(activity) && spec2->isSatisfiedBy(activity);
}

OrSpecification::OrSpecification(std::shared_ptr<ActivitySpecification> s1, std::shared_ptr<ActivitySpecification> s2)
    : spec1(s1), spec2(s2) {}

bool OrSpecification::isSatisfiedBy(const std::shared_ptr<Activity>& activity) const {
    return spec1->isSatisfiedBy(activity) || spec2->isSatisfiedBy(activity);
}
