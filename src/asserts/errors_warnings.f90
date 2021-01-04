module errors_warnings
    use precision, only: dp
    implicit none
    private

    public :: handle_open_error
contains

    !> Handle integer open errors returned by the iostat option
    !> of the open subroutine
    subroutine handle_open_error(ierr, silent_error)
        !> Error integer returned by iostat
        integer, intent(in) :: ierr
        !> Report error but don't kill the code. Default is to kill the code
        logical, intent(in), optional :: silent_error

        logical :: kill

        kill = .true.
        if (present(silent_error)) then
            if (silent_error) kill = .false.
        end if

        ! select case would be more readable
        if (ierr == 0) then
            return

        else if (ierr == -1) then
            write(*, *) 'open file error. end-of-file condition occurred'
            if (kill) stop

        else if (ierr == -2) then
            write(*, *) 'open file error. end-of-record condition occurred with non-advancing reads'
            if (kill) stop

        else
            write(*, *) 'open file error. Error code ', ierr
            !TODO(Alex) Tabulate most common errors or see if someone's already wrapped them
            write(*, *) 'See reference link in error_warnings'
            !https://scc.ustc.edu.cn/zlsc/tc4600/intel/2015.1.133/compiler_f/GUID-44448B78-2B87-4998-9828-C8BAEB9F5C9A.htm#GUID-44448B78-2B87-4998-9828-C8BAEB9F5C9A
            if (kill) stop
        end if

    end subroutine handle_open_error

end module errors_warnings