package examples

import (
	"fmt"
	"math"
)

// SankhyaExample demonstrates basic statistical calculations
type SankhyaExample struct {
	data []float64
}

// NewSankhyaExample creates a new instance with sample data
func NewSankhyaExample() *SankhyaExample {
	return &SankhyaExample{
		data: []float64{1.0, 2.0, 3.0, 4.0, 5.0},
	}
}

// CalculateMean returns the arithmetic mean of the data
func (s *SankhyaExample) CalculateMean() float64 {
	sum := 0.0
	for _, value := range s.data {
		sum += value
	}
	return sum / float64(len(s.data))
}

// CalculateVariance returns the variance of the data
func (s *SankhyaExample) CalculateVariance() float64 {
	mean := s.CalculateMean()
	sumSquaredDiff := 0.0

	for _, value := range s.data {
		diff := value - mean
		sumSquaredDiff += diff * diff
	}

	return sumSquaredDiff / float64(len(s.data))
}

// CalculateStandardDeviation returns the standard deviation
func (s *SankhyaExample) CalculateStandardDeviation() float64 {
	return math.Sqrt(s.CalculateVariance())
}

// PrintStatistics prints all calculated statistics
func (s *SankhyaExample) PrintStatistics() {
	fmt.Printf("Data: %v\n", s.data)
	fmt.Printf("Mean: %.2f\n", s.CalculateMean())
	fmt.Printf("Variance: %.2f\n", s.CalculateVariance())
	fmt.Printf("Standard Deviation: %.2f\n", s.CalculateStandardDeviation())
}
