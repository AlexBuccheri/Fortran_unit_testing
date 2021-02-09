!> Assertions for use in debug mode
module asserts
    use iso_fortran_env, only: error_unit
    implicit none
    private

    !> Error code for false assertions
    integer, parameter :: assert_error_code = -101

    !>  A generic interface for assertions
    Interface assert
        Module Procedure assert_true
    End Interface assert

    public :: assert

contains

    !> @todo(Alex) Make thread-safe and MPI-safe w.r.t. printing and potentially stopping
    !> Assert if a logical condition is true
    !>
    !> If not compiled with USE_ASSERT, the compiler is smart enough
    !> to remove the routine, which will be empty i.e. no overhead
    subroutine assert_true(logical_condition, message)
        !> Condition to test
        logical, intent(in) :: logical_condition
        !> Optional error message
        character(len=*), intent(in), optional :: message
#ifdef USE_ASSERT
        if (.not. logical_condition) then
            if (present(message)) then
                write (error_unit, '(/,1x,a)') trim(adjustl(message))
            endif

            !TODO(Alex) Would rather return an error than immediately stop the code
            !stop assert_error_code
        end if
#endif
    end subroutine assert_true


end module asserts