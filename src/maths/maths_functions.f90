module maths_functions
    use precision, only: wp
    implicit none
    private

    public :: sgn

contains

    !> sgn function
    !>   -1 & \text{if~} x < 0   \\
    !>    0 & \text{if~} x = 0   \\
    !>   +1 & \text{if~} x > 0
    real(wp) function sgn(x) result(sgn_value)
        real(wp), intent(in) :: x

        sgn_value = 0._wp
        if (x > 0._wp) then
            sgn_value = 1._wp
        else if (x < 0._wp) then
            sgn_value = -1._wp
        end if

    end function sgn

end module maths_functions