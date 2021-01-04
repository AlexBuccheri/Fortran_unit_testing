!> Read various data formats
module read
    use precision, only: dp
    use asserts, only: assert
    use errors_warnings, only: handle_open_error
    implicit none
    private

    !> Maximum length for an atomic symbol
    integer, public, parameter :: len_max_sym = 2

    public :: read_xyz

contains

    !> Read .xyz format
    !> Atomic positions always defined in Angstrom for xyz format
    subroutine read_xyz(file_name, positions, species)
        !> File name
        character(len=*), intent(in) :: file_name
        !> Atomic positions
        real(dp), allocatable, intent(inout) :: positions(:, :)
        !> Atomic species
        character(len=len_max_sym), allocatable, intent(inout) :: species(:)

        integer :: ia, n_atoms, ierr
        character(len=100) :: comment
        integer :: unit

        !F2008 feature http://fortranwiki.org/fortran/show/newunit
        open(newunit=unit, file=trim(adjustl(file_name)), status='OLD', access='SEQUENTIAL', iostat=ierr)
        call handle_open_error(ierr)

        ! First line
        read(unit, *) n_atoms

        ! Second line = optional comment, else whiteline
        read(unit, *)

        ! Might be better to make intent(out)?
        if (allocated(positions)) then
            call assert(size(positions, 1) == 3, &
                    "atomic positions expected as positions(3, n_atoms)")
            call assert(size(positions, 2) == n_atoms, &
                    "size(positions) inconsistent with n_atoms in .xyz")
        else
            allocate(positions(3, n_atoms))
        end if

        if (allocated(species)) then
            call assert(size(species) == n_atoms, &
                    "size(species) inconsistent with n_atoms in .xyz")
        else
            allocate(species(n_atoms))
        end if

        ! Rest of file
        do ia = 1, n_atoms
            read(unit, *) species(ia), positions(1:3, ia)
        end do

        close(unit)

    end subroutine read_xyz

end module read